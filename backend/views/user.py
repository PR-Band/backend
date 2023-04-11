from http import HTTPStatus

from flask import Blueprint, abort, jsonify, request

from backend import schemas
from backend.storages.products import Pgstorage
from backend.storages.user import UserStorage

view = Blueprint('user', __name__)

storage = UserStorage()
pgstorage = Pgstorage()


@view.post('/')
def add_user():
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST)
    payload['id'] = -1
    new_user = schemas.User(**payload)
    user = storage.add(new_user.tgid, new_user.username)
    return jsonify(schemas.User.from_orm(user).dict()), 200


@view.get('/telegram/<int:uid>')
def get_by_tgid(uid):
    user = storage.get_by_tgid(tgid=uid)
    return jsonify(schemas.User.from_orm(user).dict())


@view.get('/<int:uid>/products/')
def get_products(uid):
    products = pgstorage.get_products(user_id=uid)
    products_user = [
        schemas.Product.from_orm(product).dict()
        for product in products
    ]
    return jsonify(products_user)
