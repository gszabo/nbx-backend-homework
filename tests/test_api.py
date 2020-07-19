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


class TestCreateUser:
    async def test_response_contains_given_data(self, client):
        input_data = {"name": "User_A", "email": "email_a@example.com"}

        create_response = await client.post("/users", json=input_data)
        assert create_response.status == 201

        response_data = await create_response.json()

        assert response_data["name"] == input_data["name"]
        assert response_data["email"] == input_data["email"]

    async def test_only_uses_email_and_name_from_input(self, client):
        input_data = {"name": "User_A", "email": "email_a@example.com", "age": 42}

        create_response = await client.post("/users", json=input_data)
        response_data = await create_response.json()

        assert "age" not in response_data


class TestGetUser:
    async def test_user_not_found_responds_with_404(self, client):
        resp = await client.get("/users/nouser")

        assert resp.status == 404

    async def test_user_exists_responds_with_user_data(self, client):
        create_response = await client.post(
            "/users", json={"name": "User_A", "email": "email_a@example.com"}
        )
        user_data = await create_response.json()

        get_user_response = await client.get("/users/" + user_data["id"])
        get_user_data = await get_user_response.json()

        assert get_user_response.status == 200
        assert get_user_data == user_data


class TestUpdateUser:
    async def test_user_not_found_responds_with_404(self, client):
        resp = await client.put("/users/nouser", json={})

        assert resp.status == 404

    async def test_update_name(self, client):
        create_response = await client.post(
            "/users", json={"name": "User_A", "email": "email_a@example.com"}
        )
        user_data = await create_response.json()

        update_user_response = await client.put(
            "/users/" + user_data["id"], json={"name": "Renamed_User_A"}
        )

        assert update_user_response.status == 200
        updated_user_data = await update_user_response.json()

        get_user_response = await client.get("/users/" + user_data["id"])
        get_user_data = await get_user_response.json()

        assert updated_user_data == get_user_data
        assert updated_user_data["name"] == "Renamed_User_A"
        assert updated_user_data["email"] == "email_a@example.com"

    async def test_update_email(self, client):
        create_response = await client.post(
            "/users", json={"name": "User_A", "email": "email_a@example.com"}
        )
        user_data = await create_response.json()

        update_user_response = await client.put(
            "/users/" + user_data["id"], json={"email": "email_a2@example.com"}
        )

        assert update_user_response.status == 200
        updated_user_data = await update_user_response.json()

        get_user_response = await client.get("/users/" + user_data["id"])
        get_user_data = await get_user_response.json()

        assert updated_user_data == get_user_data
        assert updated_user_data["name"] == "User_A"
        assert updated_user_data["email"] == "email_a2@example.com"

    async def test_id_and_other_fields_are_ignored(self, client):
        create_response = await client.post(
            "/users", json={"name": "User_A", "email": "email_a@example.com"}
        )
        original_user_data = await create_response.json()

        update_user_response = await client.put(
            "/users/" + original_user_data["id"], json={"id": "id42", "age": 42}
        )
        assert update_user_response.status == 200
        updated_user_data = await update_user_response.json()

        assert updated_user_data == original_user_data

        other_id_response = await client.get("/users/id42")
        assert other_id_response.status == 404


class TestDeleteUser:
    async def test_user_not_found_responds_with_404(self, client):
        resp = await client.delete("/users/nouser", json={})

        assert resp.status == 404

    async def test_user_exists_deletes_and_responds_with_204(self, client):
        create_response = await client.post(
            "/users", json={"name": "User_A", "email": "email_a@example.com"}
        )
        user_data = await create_response.json()

        resp = await client.delete("/users/" + user_data["id"])

        assert resp.status == 204

        all_users_response = await client.get("/users")
        all_users = await all_users_response.json()

        assert all_users == []
