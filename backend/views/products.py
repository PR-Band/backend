from http import HTTPStatus

from flask import Blueprint, abort, jsonify, request

from backend import schemas
from backend.storages.products import Pgstorage

view = Blueprint('products', __name__)


pgstorage = Pgstorage()


# Вывести список всех товаров
@view.get('/')
def get_all_products():
    # возвращаем список объектов и статус код 200 ОК
    products = pgstorage.get_all()
    new_product = [
        schemas.Product.from_orm(product).dict()
        for product in products
    ]
    return jsonify(new_product), 200


# Получить данные о конкретном товаре
@view.get('/<string:uid>')
def get_product_by_id(uid):
    # возвращаем найденный объект
    product = pgstorage.get_by_id(uid)
    return jsonify(schemas.Product.from_orm(product).dict()), 200


# Добавить новый товар
@view.post('/')
def add_product():
    # получить тело запроса можно с помощью модуля request

    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST)

    payload['id'] = -1
    new_product = schemas.Product(**payload)

    # должны вернуть созданный у нас объект
    product = pgstorage.add(new_product.title, new_product.category_id)
    return jsonify(schemas.Product.from_orm(product).dict()), 200


# Обновить данные продукта
@view.put('/<string:uid>')
def update_product(uid):
    # должны вернуть измененный объект
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST)

    new_product = schemas.Product(**payload)
    product = pgstorage.update(
        uid,
        title=new_product.title,
        category_id=new_product.category_id,
    )
    return jsonify(schemas.Product.from_orm(product).dict()), 200


# Удалить показатель
@view.delete('/<string:uid>')
def delete_product(uid):
    # ничего не возвращаем, 204 - NO CONTENT
    pgstorage.delete(uid)
    return {}, 204
