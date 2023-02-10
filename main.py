from aiohttp import web

from yolo.handler import ObjectDetecter
from api.router import set_routes as set_yolo_app_routes
from api.settings import config
from api.db.accessor import PostgresAccessor


def setup_config(application):
    application["config"] = config


def setup_accessors(application):
    application["db"] = PostgresAccessor()
    application["db"].setup(application)


def setup_handlers(application):
    application['detect_predictor'] = ObjectDetecter()


def set_routes(application):
    set_yolo_app_routes(application)


def setup_app(application):
    setup_config(application)
    setup_accessors(application)
    setup_handlers(application)
    set_routes(application)


app = web.Application()

if __name__ == "__main__":
    setup_app(app)
    web.run_app(app, port=app['config']["app_port"])
