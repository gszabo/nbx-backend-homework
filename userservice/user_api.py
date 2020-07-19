import uuid


class UserAPI:
    def __init__(self):
        self._users = {}

    def get_users(self):
        return list(self._users.values())

    def get_user(self, id_):
        return self._users.get(id_)

    def create_user(self, user_params):
        id_ = str(uuid.uuid4())
        new_user = {
            "id": id_,
            "name": user_params["name"],
            "email": user_params["email"],
        }
        self._users[id_] = new_user
        return new_user

    def update_user(self, id_, update_params):
        if id_ not in self._users:
            return None

        user = self._users[id_]

        if "name" in update_params:
            user["name"] = update_params["name"]
        if "email" in update_params:
            user["email"] = update_params["email"]

        return user

    def delete_user(self, id_):
        return self._users.pop(id_, None)
