from http import HTTPStatus

from flask import Blueprint, abort, jsonify, request

from backend import schemas
from backend.storages.categories import PgstorageCategory

view = Blueprint('categories', __name__)

pgstorage = PgstorageCategory()


@view.get('/')
def get_all_categories():
    args = request.args
    args_title = args.get('search')
    if args_title:
        categories = pgstorage.search_by_name(args_title)
        new_categories = [
            schemas.Category.from_orm(category).dict()
            for category in categories
        ]
        return jsonify(new_categories), 200

    args_title = args.get('title')
    if args_title:
        categories = pgstorage.get_by_name(args_title)
        new_categories = [
            schemas.Category.from_orm(category).dict()
            for category in categories
        ]
        return jsonify(new_categories), 200

    categories = pgstorage.get_all()
    new_categories = [
        schemas.Category.from_orm(category).dict()
        for category in categories
    ]
    return jsonify(new_categories), 200


@view.get('/<string:uid>')
def get_category_by_id(uid):
    category = pgstorage.get_by_id(uid)
    return jsonify(schemas.Category.from_orm(category).dict()), 200


@view.post('/')
def add_category():
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST)
    payload['id'] = -1
    new_category = schemas.Category(**payload)

    category = pgstorage.add(new_category.title)
    return jsonify(schemas.Category.from_orm(category).dict()), 200


@view.put('/<string:uid>')
def update_category(uid):
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST)

    new_category = schemas.Category(**payload)
    category = pgstorage.update(uid, title=new_category.title)
    return jsonify(schemas.Category.from_orm(category).dict()), 200


@view.delete('/<string:uid>')
def delete_category(uid):
    pgstorage.delete(uid)

    return {}, 204
