from flask import Flask, jsonify, request, abort
from http import HTTPStatus
from uuid import uuid4

app = Flask(__name__)


categories = [
    {"id": uuid4().hex,
     "title": "Тренировки по волейболу"},
    {"id": uuid4().hex,
     "title": "Массаж"}
]

# storage = {}
# for category in categories:
#     storage[category['id']] = category

storage = {category['id']: category for category in categories}

@app.get('/api/v1/categories/')
def get_all_categories():
    # возвращаем список обьектов и статус код 200 OK
    return jsonify(list(storage.values())), 200


@app.get('/api/v1/categories/<string:uid>')
def get_category_by_id(uid):
    # возвращаем найденный обьект
    category = storage.get(uid)
    if category:
        return jsonify(category), 200
    abort(404)


@app.post('/api/v1/category/')
def add_category():
    # получить тело запроса можно с помощью модуля request
    # payload = request.json()
    category = request.json
    category['id'] = uuid4().hex
    storage[category['id']] = category
    # должны вернуть созданный у нас объект
    return jsonify(category), 200


@app.put('/api/v1/categories/<string:uid>')
def update_category(uid):
    # должны вернуть измененный объект
    category = storage.get(uid)
    if uid not in storage:
        abort(404)

    payload = request.json
    category.update(payload)
    return jsonify(category), 200


@app.delete('/api/v1/categories/<string:uid>')
def delete_category(uid):
    # ничего не возвращаем, 204 - NO CONTENT
    if uid not in storage:
        abort(404)

    storage.pop(uid)
    return {}, 204
