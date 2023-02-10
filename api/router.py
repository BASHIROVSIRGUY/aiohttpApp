from aiohttp import web
from api.views import PictureItemView, PictureCollectionView, UserItemView, UserCollectionView

def set_routes(app: web.Application) -> None:
    app.router.add_view('/user', UserCollectionView)
    app.router.add_view('/user/{pk}', UserItemView)
    app.router.add_view('/user/{user_pk}/picture', PictureCollectionView)
    app.router.add_view('/user/{user_pk}/picture/{pk}', PictureItemView)

