from typing import List, Union
from uuid import UUID

from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200, r201, r204, r404

from api.schemas import PictureRequest, PictureResponse, User, Error


################################################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~ Picture ~~~~~~~~~~~~~~~~~~~~~~~~~~ #
################################################################


class PictureCollectionView(PydanticView):
    async def get(self) -> r200[List[PictureResponse]]:
        pictures = await self.request.app["db"].picture_model.read_all()
        return web.json_response([picture.dict() for picture in pictures])

    async def post(self, user_pk: UUID, /, picture: PictureRequest) -> r201[PictureResponse]:
        picture = await self.request.app["db"].picture_model.create(picture, user_pk)
        return web.json_response(picture.dict())


class PictureItemView(PydanticView):
    async def get(self, pk: UUID, /) -> Union[r200[PictureResponse], r404[Error]]:
        picture = await self.request.app["db"].picture_model.read(pk)
        return web.json_response(picture.dict())

    async def put(self, pk: UUID, /, picture: PictureResponse) -> r200[PictureResponse]:
        await self.request.app["db"].picture_model.update(pk, picture)
        return web.json_response(picture.dict())

    async def remove(self, pk: UUID, /) -> r204:
        await self.request.app["db"].picture_model.remove(pk)
        return web.Response(status=204)


################################################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ User ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
################################################################


class UserCollectionView(PydanticView):
    async def get(self) -> r200[List[User]]:
        users = await self.request.app["db"].user_model.read_all()
        return web.json_response([user.dict() for user in users])

    async def post(self, user: User) -> r201[User]:
        await self.request.app["db"].user_model.create(user)
        return web.json_response(user.dict())


class UserItemView(PydanticView):
    async def get(self, pk: UUID, /) -> Union[r200[User], r404[Error]]:
        user = await self.request.app["db"].user_model.read(pk)
        return web.json_response(user.dict())

    async def put(self, pk: UUID, /, user: User) -> r200[User]:
        await self.request.app["db"].user_model.update(pk, user)
        return web.json_response(user.dict())

    async def remove(self, pk: UUID, /) -> r204:
        await self.request.app["db"].user_model.remove(pk)
        return web.Response(status=204)
