from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr


class Users(BaseModel):
    id_user: Optional[int] = None
    login: str
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str
    avatar: Optional[str] = None
    id_role: int
    time: int

    def is_admin(self):
        return self.id_role == 1


class UserIn(BaseModel):
    login: str
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str
    id_role: int

