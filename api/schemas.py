import re
from uuid import UUID
from enum import Enum
from pydantic import BaseModel, EmailStr, validator

NAME_REG_PATTERN = re.compile(r"[A-zА-яЁё\-\s]+")


class PictureType(str, Enum):
    png = 'png'
    jpeg = 'jpg'


class AbstractModel(BaseModel):
    class Config:
        orm_mode = True


class PictureRequest(AbstractModel):
    in_img: bytes
    img_type: PictureType


class PictureResponse(PictureRequest):
    out_img: bytes
    user_id: UUID


class User(AbstractModel):
    name: str
    email: EmailStr

    @validator('name')
    def check_name(cls, val):
        if not NAME_REG_PATTERN.match(val):
            raise ValueError('Name must contain only letters, \' \' or \'-\'')
        return val


class Error(BaseModel):
    error: str
