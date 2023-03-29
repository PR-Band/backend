from http import HTTPStatus

from flask import Blueprint, abort, jsonify, request

from backend import schemas
from backend.storages.user import UserStorage

view = Blueprint('user', __name__)

storage = UserStorage()


@view.post('/')
def add_user():
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST)
    payload['id'] = -1
    new_user = schemas.User(**payload)
    user = storage.add(new_user.tgid, new_user.username)
    return jsonify(schemas.User.from_orm(user).dict()), 200
