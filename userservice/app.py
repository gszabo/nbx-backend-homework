import logging
import uuid

from aiohttp import web

from userservice.user_api import UserAPI

LOGGER = logging.getLogger(__name__)


routes = web.RouteTableDef()

api = UserAPI()


@routes.get("/")
async def health(request):
    return web.json_response({"name": "user-service"})


@routes.get("/users")
async def get_users(request):
    return web.json_response(api.get_users())


@routes.get("/users/{user_id}")
async def get_user(request):
    user = api.get_user(request.match_info["user_id"])
    if user:
        return web.json_response(user)
    else:
        raise web.HTTPNotFound()


@routes.post("/users")
async def create_user(request):
    new_user = api.create_user(await request.json())
    return web.json_response(new_user, status=201)


@routes.put("/users/{user_id}")
async def update_user(request):
    id_ = request.match_info["user_id"]
    body = await request.json()

    updated_user = api.update_user(id_, body)

    if not updated_user:
        raise web.HTTPNotFound()

    return web.json_response(updated_user)


@routes.delete("/users/{user_id}")
async def delete_user(request):
    id_ = request.match_info["user_id"]
    user = api.delete_user(id_)
    if not user:
        raise web.HTTPNotFound()
    return web.json_response(None, status=204)


@routes.delete("/users")
async def delete_users(request):
    api._users = {}
    return web.json_response(None, status=204)


def create_app():
    app = web.Application()
    app.add_routes(routes)
    return app
