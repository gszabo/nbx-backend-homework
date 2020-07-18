At this point we have an in memory implementation of the User API. The code
is scattered among the request handlers, but we have tests that hit the HTTP API
and can help with refactoring.

Things I would like to add:
- run tests in random order
- extract logic from request handlers
    - delete the `DELETE /users` endpoint that deletes all users. It is there
    to help with testing, but I expect to solve this differently when the
    logic is extracted from the request handlers.
- use dataclasses instead of dicts internally (eg. for User, UserCreation and UserUpdate payloads)
- use schemas to validate input and serialize users
    - input validation:
        - email addresses are well formatted
        - names have a minimum length
