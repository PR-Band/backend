from http import HTTPStatus
from uuid import uuid4

from flask import Blueprint, abort, jsonify, request

from backend.storages.products import ProductsStorage

view = Blueprint('products', __name__)

init_products = [
    {'id': uuid4().hex,
     'title': 'Тренировки по волейболу',
     },
    {'id': uuid4().hex,
     'title': 'Массаж',
     },
]

storage = ProductsStorage(init_products)


# Вывести список всех товаров
@view.get('/')
def get_all_products():
    # возвращаем список объектов и статус код 200 ОК
    return jsonify(storage.get_all()), 200


# Получить данные о конкретном товаре
@view.get('/<string:uid>')
def get_product_by_id(uid):
    # возвращаем найденный объект
    product = storage.get_by_id(uid)
    if product:
        return jsonify(product), 200
    abort(HTTPStatus.NOT_FOUND)


# Добавить новый товар
@view.post('/')
def add_product():
    # получить тело запроса можно с помощью модуля request

    new_product = request.json
    if not new_product:
        abort(HTTPStatus.BAD_REQUEST)
    # должны вернуть созданный у нас объект
    return jsonify(storage.add(new_product)), 200


# Обновить данные продукта
@view.put('/<string:uid>')
def update_product(uid):
    # должны вернуть измененный объект
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST)

    product = storage.update(payload, uid)
    if not product:
        abort(HTTPStatus.NOT_FOUND)

    return jsonify(product), 200


# Удалить показатель
@view.delete('/<string:uid>')
def delete_product(uid):
    # ничего не возвращаем, 204 - NO CONTENT
    storage.delete(uid)
    if not storage.delete(uid):
        abort(HTTPStatus.NOT_FOUND)
    return {}, 204
