from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.service.main import ProductFractal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()
fractal = ProductFractal()


class TokenPayload(BaseModel):
    iss: Optional[str]
    sub: Optional[UUID]
    account: Optional[UUID]
    email: Optional[str]
    typ: Optional[str]


def get_payload(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    return TokenPayload(**fractal.context.token_service.verify(token))
