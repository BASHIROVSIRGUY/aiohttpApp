from aiohttp import web

from api.db.models import Base
from api.db.handlers import PictureHandler, UserHandler
from api.db.connect import create_session


class PostgresAccessor:
    def __init__(self):
        self.session = None

    def setup(self, application: web.Application):
        application.on_startup.append(self._on_connect)
        application.on_cleanup.append(self._on_disconnect)

    async def _on_connect(self, application: web.Application):
        self.session = await create_session(
            database_url=application["config"]["database_url"],
            base=Base
        )
        await self._set_models(application)

    async def _on_disconnect(self, _):
        if self.session is not None:
            await self.session.close()

    async def _set_models(self, application: web.Application):
        self.picture_model = PictureHandler(
            session=self.session,
            detect_predictor=application['detect_predictor']
        )
        self.user_model = UserHandler(session=self.session)


