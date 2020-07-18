from operator import itemgetter

from userservice.app import create_app

import pytest


@pytest.fixture
def client(loop, aiohttp_client):
    app = create_app()
    return loop.run_until_complete(aiohttp_client(app))


@pytest.fixture(autouse=True)
async def delete_users(client):
    await client.delete("/users")

async def test_healthcheck(client):
    resp = await client.get("/")
    assert resp.status == 200
    body = await resp.json()
    assert {"name": "user-service"} == body


class TestListUsers:
    async def test_after_creation_returns_all_users(self, client):
        create_response_1 = await client.post(
            "/users", json={"name": "User_A", "email": "email_a@example.com"}
        )
        create_response_2 = await client.post(
            "/users", json={"name": "User_B", "email": "email_b@example.com"}
        )

        user_data_1 = await create_response_1.json()
        user_data_2 = await create_response_2.json()

        all_users_response = await client.get("/users")
        all_users_data = await all_users_response.json()

        assert sorted(all_users_data, key=itemgetter("name")) == [
            user_data_1,
            user_data_2,
        ]

    async def test_no_user_created_returns_empty_list(self, client):
        resp = await client.get("/users")

        assert resp.status == 200
        body = await resp.json()
        assert [] == body
