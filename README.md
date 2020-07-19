# NBX Backend Recruitment Assignment

Welcome to the NBX developer assignment! The goal of this project to get an idea of your coding style. Enjoy!

## Requirements

This is a User Service API. It's purpose is to manage user resources. It should provide JSON endpoints to do this.

### Endpoints

- health: `GET /` - this is just an endpoint that returns the service name. You can hit this once you bring up the service to make sure it's working.
- list users: `GET /users` - return the list of users
  - Response Body:

    ```json
    [{
        "id": "uuid",
        "name": "string",
        "email": "string"
    }]
    ```

- create user: `POST /users` - create a user with the given request payload
  - Request Body:

    ```json
    {
        "name": "string",
        "email": "string"
    }
    ```

  - Response Body:

    ```json
    {
        "id": "uuid",
        "name": "string",
        "email": "string"
    }
    ```

- get user by id: `GET /users/{user_id}` - return the user with the ID from the url, or 404 if not found
  - Response Body:

    ```json
    {
        "id": "uuid",
        "name": "string",
        "email": "string"
    }
    ```

- update a user: `PUT /users/{user_id}` - update the user with the provided ID with the request payload, or 404 if not found
  - Request Body:

    ```json
    {
        "id": "uuid",
        "name": "string",
        "email": "string"
    }
    ```

  - Response Body:

    ```json
    {
        "id": "uuid",
        "name": "string",
        "email": "string"
    }
    ```

- delete a user: `DELETE /users/{user_id}` - delete the user with the given ID
  - Response: 204 No Content

## Possible Extras

- input validation
- unit tests (if you do this, add a section to this README with details on how to run them)
- functional tests (if you do this, add a section to this README with details on how to run them)
- use a database to store user resources
- restructure files to be more maintainable
- UI
- Error handling

## Prerequisites

- Docker: https://docs.docker.com/install/

## How to run the project

### Build

From within the project, run `docker-compose build`

### Run

From within the project, run `docker-compose up -d app`

### Verify the service is up and running

Running `curl http://localhost:8080` should return `{"name": "user-service"}`

### Apply Changes

After you've made changes, run the above two commands again

### View logs

From within the project, run `docker-compose logs -f app`

## Solution comments

### Scope

Apart from the required functionality, I added from the extras:
- tests (HTTP endpoint based tests, so they are more or less functional tests)
- input validation
- separated user management logic from web request handlers

### Approach

The git history should give an idea about how I approached the problem. I went through
roughly these steps:

1. First, I implemented the functionality inside the request handlers with a global dictionary
object. At this stage I tested the endpoints manually, with `curl`.
2. Then I set up the infrastructure to run tests. I created some HTTP endpoint
based tests to cover me during refactoring. To isolate the tests, I added a
new endpoint that let me clear the "user database" for each test.
3. With the tests acting as a safety net, I extracted the user management logic
into its own module. Then I replaced the global variable with an instance of the
API class injected into the `app` instance. This allowed me to inject a new,
fresh instance into every test, so I deleted the "clear database" endpoint created
earlier for the tests.
4. After that I introduced a dataclass holding the user information and changed
the API internally to store that kind of objects.
5. Lastly, I created schema descriptor classes to serialize User objects and
deserialize and validate input data (for user creation and update).

### Run tests

For the time being there are no separate unit and functional tests. To run
_the tests_ issue the command:
```
docker-compose run test
```

The tests are run in a randomized order.
