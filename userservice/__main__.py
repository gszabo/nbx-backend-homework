import logging

from aiohttp import web

from userservice.app import create_app
from userservice.user_api import UserAPI

LOGGER = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    app = create_app()
    app['userservice.api'] = UserAPI()

    LOGGER.info("### Starting user service ###")
    web.run_app(app)
