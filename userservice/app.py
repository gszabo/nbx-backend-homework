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


@routes.post('/users')
async def create_user(request):
    body = await request.json()
    id_ = uuid.uuid4()
    new_user = {"name": body["name"], "id": str(id_), "email": body["email"]}
    users[id_] = new_user
    return web.json_response(new_user, status=201)


@routes.put('/users/{user_id}')
async def update_user(request):
    return web.json_response({})


@routes.delete('/users/{user_id}')
async def delete_user(request):
    return web.json_response(None, status=204)


def create_app():
    app = web.Application()
    app.add_routes(routes)
    return app
