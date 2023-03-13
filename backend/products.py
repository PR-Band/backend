from http import HTTPStatus
from uuid import uuid4

from flask import Blueprint, abort, jsonify, request

view = Blueprint('products', __name__)

storage = [
    {
        'id': uuid4().hex,
        'tytle': 'тренировки по волейболу',
        'category': 'что-то',
    },
    {
        'id': uuid4().hex,
        'tytle': 'Услуги массажа',
        'category': 'что-то',
    },
]


# Вывести список всех товаров
@view.get('/')
def get_all_products():
    # возвращаем список объектов и статус код 200 ОК
    return jsonify({'products': storage}), 200


# Получить данные о конкретном товаре
@view.get('/<string:uid>')
def get_product_by_id(uid):
    # возвращаем найденный объект
    for diction in storage:
        if diction['id'] == uid:
            return jsonify(diction), 200
    abort(HTTPStatus.NOT_FOUND)
# Добавить новый товар


@view.post('/')
def add_product():
    # получить тело запроса можно с помощью request payload = request.json()
    product = {
        'id': uuid4().hex,
        'title': request.json['title'],
        'category': request.json.get('category', ''),
    }
    storage.append(product)
    # должны вернуть созданный у нас объект
    return jsonify(product), 200


@view.put('/<string:uid>')
def update_product(uid):
    for diction in storage:
        if diction['id'] == uid:
            diction['title'] = request.json.get('title', diction['title'])
            diction['category'] = request.json.get('category', diction['category'])
        return diction, 200


@view.delete('/<string:uid>')
def delete_product(uid):
    for diction in storage:
        if diction['id'] == uid:
            storage.remove(diction)
    # ничего не возвращаем, 204 - NO CONTENT
    return {}, 204
