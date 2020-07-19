import logging

from aiohttp import web

from userservice.user_api import UserAPI


routes = web.RouteTableDef()


@routes.get("/")
async def health(request: web.Request):
    return web.json_response({"name": "user-service"})


@routes.get("/users")
async def get_users(request: web.Request):
    return web.json_response(_get_api(request).get_users())


@routes.get("/users/{user_id}")
async def get_user(request: web.Request):
    user = _get_api(request).get_user(request.match_info["user_id"])
    if user:
        return web.json_response(user)
    else:
        raise web.HTTPNotFound()


@routes.post("/users")
async def create_user(request: web.Request):
    new_user = _get_api(request).create_user(await request.json())
    return web.json_response(new_user, status=201)


@routes.put("/users/{user_id}")
async def update_user(request: web.Request):
    id_ = request.match_info["user_id"]
    body = await request.json()

    updated_user = _get_api(request).update_user(id_, body)

    if not updated_user:
        raise web.HTTPNotFound()

    return web.json_response(updated_user)


@routes.delete("/users/{user_id}")
async def delete_user(request: web.Request):
    id_ = request.match_info["user_id"]
    user = _get_api(request).delete_user(id_)
    if not user:
        raise web.HTTPNotFound()
    return web.json_response(None, status=204)


def _get_api(request: web.Request) -> UserAPI:
    return request.app["userservice.api"]


def create_app():
    app = web.Application()
    app.add_routes(routes)
    return app
