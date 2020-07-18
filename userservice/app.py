import logging
from aiohttp import web
import uuid


LOGGER = logging.getLogger(__name__)


routes = web.RouteTableDef()


users = {}


@routes.get('/')
async def health(request):
    return web.json_response({'name': 'user-service'})


@routes.get('/users')
async def get_users(request):
    return web.json_response(list(users.values()))

@routes.get('/users/{user_id}')
async def get_user(request):
    id_ = request.match_info["user_id"]
    if id_ in users:
        return web.json_response(users[id_])
    else:
        raise web.HTTPNotFound()

@routes.post('/users')
async def create_user(request):
    body = await request.json()
    id_ = str(uuid.uuid4())
    new_user = {"name": body["name"], "id": id_, "email": body["email"]}
    users[id_] = new_user
    return web.json_response(new_user, status=201)


@routes.put('/users/{user_id}')
async def update_user(request):
    id_ = request.match_info["user_id"]
    if id_ not in users:
        raise web.HTTPNotFound()

    user = users[id_]
    body = await request.json()
    if "name" in body:
        user["name"] = body["name"]
    if "email" in body:
        user["email"] = body["email"]

    return web.json_response(user)


@routes.delete('/users/{user_id}')
async def delete_user(request):
    id_ = request.match_info["user_id"]
    if id_ not in users:
        raise web.HTTPNotFound()
    del users[id_]
    return web.json_response(None, status=204)


def create_app():
    app = web.Application()
    app.add_routes(routes)
    return app
