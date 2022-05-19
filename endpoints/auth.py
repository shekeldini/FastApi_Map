from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends, Response, Cookie
from models.token import Token, Login, AccessToken
from repositories.users import UsersRepository
from core.security import verify_password, create_access_token, create_refresh_token
from .depends import get_users_repository, get_current_user

router = APIRouter()


@router.post("/", response_model=Token)
async def login(
        login: Login,
        response: Response,
        users: UsersRepository = Depends(get_users_repository)
):
    user = await users.get_by_login(login.login)
    if user is None or not verify_password(login.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = Token(
        access_token=create_access_token({"sub": user.login}),
        refresh_token=create_refresh_token({"sub": user.login}),
        token_type="Bearer"
    )
    response.set_cookie(
        key="refresh_token", value=f"{token.refresh_token}", httponly=True, secure=True, samesite="strict"
    )
    return token


@router.post('/refresh', response_model=AccessToken)
async def refresh(refresh_token: Optional[str] = Cookie(None)):
    current_user = await get_current_user(users=get_users_repository(), token=refresh_token)
    new_token = create_access_token({"sub": current_user.login})
    return AccessToken(access_token=new_token)
