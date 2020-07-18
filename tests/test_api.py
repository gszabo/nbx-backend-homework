from userservice.app import create_app

async def test_healthcheck(aiohttp_client):
    client = await aiohttp_client(create_app())
    resp = await client.get("/")
    assert resp.status == 200
    body = await resp.json()
    assert {"name": "user-service"} == body
