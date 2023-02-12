from abc import ABC, abstractmethod
from typing import List
import uuid

import asyncio
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update

from api.db.models import PictureTable, UserTable
from api.schemas import PictureRequest, PictureResponse, User


class AbstractHandler(ABC):
    def __init__(self, session):
        self.session = session

    @abstractmethod
    async def create(self, *args, **kwargs):
        pass

    @abstractmethod
    async def read(self, *args, **kwargs):
        pass

    @abstractmethod
    async def read_all(self, *args, **kwargs):
        pass

    @abstractmethod
    async def update(self, *args, **kwargs):
        pass

    @abstractmethod
    async def remove(self, *args, **kwargs):
        pass

    @abstractmethod
    async def _convert_to_schema(self, *args, **kwargs):
        pass


################################################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~ Picture ~~~~~~~~~~~~~~~~~~~~~~~~~~ #
################################################################


class PictureHandler(AbstractHandler):
    def __init__(self, session, detect_predictor):
        super().__init__(session)
        self.detect_predictor = detect_predictor

    async def create(self, user_pk: uuid.UUID, picture: PictureRequest) -> PictureResponse:
        in_img = picture.in_img
        img_type = picture.img_type
        out_img = await self._get_predict_img(in_img, img_type)
        self.session.add(
            PictureTable(in_img=in_img, out_img=out_img, img_type=img_type, user_id=user_pk)
        )
        await self.session.commit()
        return PictureResponse(
            in_img=in_img,
            out_img=out_img,
            img_type=img_type,
            user_id=user_pk
        )

    async def read(self, pk: uuid.UUID) -> PictureResponse:
        query = select(PictureTable).where(PictureTable.c.id == pk)
        result = await self.session.execute(query)
        return self._convert_to_schema(result.scalars().one())

    async def read_all(self) -> List[PictureResponse]:
        query = select(PictureTable)
        result = await self.session.execute(query)
        return [self._convert_to_schema(item) for item in result.scalars().all()]

    async def update(self, pk: uuid.UUID, picture: PictureResponse) -> None:
        query = (
            sqlalchemy_update(PictureTable)
            .where(PictureTable.c.id == pk)
            .values(in_img=picture.in_img, out_img=picture.out_img, img_type=picture.img_type, user_id=picture.user_id)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(query)
        await self.session.commit()

    async def remove(self, pk: uuid.UUID) -> None:
        query = (
            delete(PictureTable)
            .where(UserTable.c.id == pk)
        )
        await self.session.execute(query)
        await self.session.commit()

    def _convert_to_schema(self, picture_table_obj: PictureTable) -> PictureResponse:
        return PictureResponse(
            in_img=picture_table_obj.in_img,
            out_img=picture_table_obj.out_img,
            img_type=picture_table_obj.img_type,
            user_id=picture_table_obj.user_pk
        )

    async def _get_predict_img(self, img: bytes, type: str) -> bytes:
        loop = asyncio.get_running_loop()
        predict_img = await loop.run_in_executor(self.detect_predictor.detect(img, type))
        return predict_img


################################################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ User ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
################################################################


class UserHandler(AbstractHandler):
    async def create(self, user: User) -> User:
        self.session.add(
            UserTable(name=user.name, email=user.email)
        )
        await self.session.commit()
        return user

    async def read(self, pk: uuid.UUID) -> User:
        query = select(UserTable).where(UserTable.c.id == pk)
        result = await self.session.execute(query)
        return self._convert_to_schema(result.scalars().one())

    async def read_all(self) -> List[User]:
        query = select(UserTable)
        result = await self.session.execute(query)
        return [self._convert_to_schema(item) for item in result.scalars().all()]

    async def update(self, pk: uuid.UUID, user: User):
        query = (
            sqlalchemy_update(UserTable)
            .where(UserTable.c.id == pk)
            .values(name=user.name, email=user.email)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(query)
        await self.session.commit()

    async def remove(self, pk: uuid.UUID):
        query = (
            delete(UserTable)
            .where(UserTable.c.id == pk)
        )
        await self.session.execute(query)
        await self.session.commit()

    def _convert_to_schema(self, user_table_obj: UserTable) -> User:
        return User(
            name=user_table_obj.name,
            email=user_table_obj.email
        )