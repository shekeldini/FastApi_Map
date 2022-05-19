import uvicorn
import secrets

from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.templating import Jinja2Templates
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from core.security import verify_password
from db.base import database, redis
from endpoints import district, oo_location_type, roles, users, auth, name_of_the_settlement, \
    organizational_and_legal_form, population_of_the_settlement, oo_logins, organisation_status, oo
from endpoints.depends import get_users_repository
from repositories.users import UsersRepository

app = FastAPI(
    title="FastAPI",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

security = HTTPBasic()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth.router, prefix='/auth', tags=["auth"])
app.include_router(users.router, prefix='/user', tags=["users"])
app.include_router(roles.router, prefix='/roles', tags=["roles"])
app.include_router(district.router, prefix='/district', tags=["district"])
app.include_router(oo_location_type.router, prefix='/oo_location_type', tags=["oo_location_type"])
app.include_router(name_of_the_settlement.router, prefix='/name_of_the_settlement', tags=["name_of_the_settlement"])
app.include_router(organizational_and_legal_form.router, prefix='/organizational_and_legal_form',
                   tags=["organizational_and_legal_form"])
app.include_router(population_of_the_settlement.router, prefix='/population_of_the_settlement',
                   tags=["population_of_the_settlement"])
app.include_router(oo_logins.router, prefix='/oo_logins', tags=["oo_logins"])
app.include_router(organisation_status.router, prefix='/organisation_status', tags=["organisation_status"])
app.include_router(oo.router, prefix='/oo', tags=["oo"])


@app.on_event("startup")
async def startup():
    await redis.connect()
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    await redis.disconnect()


async def get_current_username(
        credentials: HTTPBasicCredentials = Depends(security),
        users: UsersRepository = Depends(get_users_repository)
):
    user = await users.get_by_login(credentials.username)
    if user is None or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    if not user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user.login


@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(username: str = Depends(get_current_username)):
    return get_redoc_html(openapi_url="/openapi.json", title="docs")


@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("map.html", {"request": request, "title": "Интерактивная карта"})


if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', reload=False)
