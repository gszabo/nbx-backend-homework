from operator import itemgetter

import pytest

from userservice.app import create_app
from userservice.user_api import UserAPI


@pytest.fixture
def client(loop, aiohttp_client):
    app = create_app()

    # this dependency injection here ensures every test starts
    # with a clean "user database"
    app["userservice.api"] = UserAPI()

    return loop.run_until_complete(aiohttp_client(app))


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

    async def test_unknown_field_in_input_responds_with_400(self, client):
        input_data = {"name": "User_A", "email": "email_a@example.com", "age": 42}

        create_response = await client.post("/users", json=input_data)
        response_text = await create_response.text()

        assert create_response.status == 400
        assert "age" in response_text
        assert "unknown" in response_text.lower()

    @pytest.mark.parametrize(
        "input_data",
        [
            {"name": "User_A", "email": "email"},
            {"name": "", "email": "email@example.com"},
            {"name": None, "email": "email@example.com"},
            {"email": "email@example.com"},
            {"name": "User_A"},
        ],
        ids=[
            "invalid email",
            "empty name",
            "null name",
            "missing name",
            "missing email",
        ],
    )
    async def test_invalid_input_responds_with_400(self, client, input_data):
        create_response = await client.post("/users", json=input_data)

        assert create_response.status == 400


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

    @pytest.mark.parametrize(
        "input_data",
        [{"email": "email"}, {"name": ""}, {"name": None}, {"id": "id42"}, {"age": 42}],
        ids=["invalid email", "empty name", "null name", "ID field", "unknown field"],
    )
    async def test_invalid_input_responds_with_400(self, client, input_data):
        create_response = await client.post(
            "/users", json={"name": "User_A", "email": "email_a@example.com"}
        )
        user_data = await create_response.json()

        update_response = await client.put("/users/" + user_data["id"], json=input_data)

        assert update_response.status == 400

        # check that user is not modified at all
        original_user_response = await client.get("/users/" + user_data["id"])
        original_user_data = await original_user_response.json()

        assert original_user_data == user_data


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
