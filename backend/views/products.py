from http import HTTPStatus
from uuid import uuid4

from flask import Blueprint, abort, jsonify, request

from backend.storages.products import Pgstorage, ProductsStorage

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
pgstorage = Pgstorage()


# Вывести список всех товаров
@view.get('/')
def get_all_products():
    # возвращаем список объектов и статус код 200 ОК
    products = pgstorage.get_all()
    new_product = [{'title': _.title, 'id': _.id} for _ in products]
    return jsonify(new_product), 200


# Получить данные о конкретном товаре
@view.get('/<string:uid>')
def get_product_by_id(uid):
    # возвращаем найденный объект
    product = pgstorage.get_by_id(uid)
    if product:
        return jsonify({'title': product.title, 'id': product.id}), 200
    abort(HTTPStatus.NOT_FOUND)


# Добавить новый товар
@view.post('/')
def add_product():
    # получить тело запроса можно с помощью модуля request

    product = request.json
    if not product:
        abort(HTTPStatus.BAD_REQUEST)
    # должны вернуть созданный у нас объект
    new_product = pgstorage.add(product['title'])
    return jsonify({'title': new_product.title, 'id': new_product.id}), 200


# Обновить данные продукта
@view.put('/<string:uid>')
def update_product(uid):
    # должны вернуть измененный объект
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST)

    product = pgstorage.update(payload, uid)
    if not product:
        abort(HTTPStatus.NOT_FOUND)
    return jsonify({'title': product.title, 'id': product.id}), 200


# Удалить показатель
@view.delete('/<string:uid>')
def delete_product(uid):
    # ничего не возвращаем, 204 - NO CONTENT
    pgstorage.delete(uid)
    # if not pgstorage.delete_product(uid):
    #     abort(HTTPStatus.NOT_FOUND)
    return {}, 204
