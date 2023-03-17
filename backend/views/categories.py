from http import HTTPStatus
from uuid import uuid4

from flask import Blueprint, abort, jsonify, request

from backend.storages.categories import CategoryStorage

view = Blueprint('categories', __name__)

init_categories = [
    {'id': uuid4().hex,
     'title': 'Тренировки по волейболу',
     },
    {'id': uuid4().hex,
     'title': 'Массаж',
     },
]

storage = CategoryStorage(init_categories)


@view.get('/')
def get_all_categories():
    categories = storage.get_all()
    return jsonify(categories), 200


@view.get('/<string:uid>')
def get_category_by_id(uid):
    category = storage.get_by_id(uid)
    if not category:
        abort(HTTPStatus.NOT_FOUND)

    return jsonify(category), 200


@view.post('/')
def add_category():
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST)

    category = storage.add(payload)

    return jsonify(category), 200


@view.put('/<string:uid>')
def update_category(uid):
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST)

    category = storage.update(uid, payload)
    if not category:
        abort(HTTPStatus.NOT_FOUND)

    return jsonify(category), 200


@view.delete('/<string:uid>')
def delete_category(uid):
    if not storage.delete(uid):
        abort(HTTPStatus.NOT_FOUND)

    return {}, 204
