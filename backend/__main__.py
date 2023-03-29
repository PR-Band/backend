import logging
from http import HTTPStatus

from flask import Flask, jsonify
from pydantic import ValidationError

from backend.db import db_session

from backend.errors import AppError, NotfoundError

from backend.views import categories, products, user

logger = logging.getLogger(__name__)

app = Flask(__name__)
APP_PORT = 8000


@app.errorhandler(AppError)
def handle_app_error(error: AppError):
    return jsonify(error=str(error)), error.status


@app.errorhandler(NotfoundError)
def handle_Notfound_error(error: NotfoundError):
    return jsonify(error=str(error)), error.status


@app.errorhandler(ValidationError)
def handle_Validation_error(error: ValidationError):
    return jsonify(error=str(error)), HTTPStatus.UNPROCESSABLE_ENTITY


def main():
    logging.basicConfig(level=logging.INFO)
    logger.info('hello world')
    app.register_blueprint(categories.view, url_prefix='/api/v1/categories')
    app.register_blueprint(products.view, url_prefix='/api/v1/products')
    app.register_blueprint(user.view, url_prefix='/api/v1/users')
    app.teardown_appcontext(shutdown_session)

    app.run(port=APP_PORT)


def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    main()
