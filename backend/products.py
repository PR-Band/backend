from flask import Flask, jsonify, request, abort
from http import HTTPStatus
from uuid import uuid4


storage = [{
        "id": uuid4().hex,
        "tytle": "тренировки по волейболу",
        "category": "что-то",
    }, {
        "id": uuid4().hex,
        "tytle": "услуги массажа",
        "category": "что-то"}]


app = Flask(__name__)
# @app.route('/')
# def server():
#     return "Привет!"

# Вывести список всех товаров
@app.get('/api/v1/products/')
def get_all_products():
    # возвращаем список объектов и статус код 200 ОК
    return jsonify({'products': storage}), 200


# Получить данные о конкретном товаре
@app.get('/api/v1/products/<string:uid>')
def get_product_by_id(uid):
    # возвращаем найденный объект
    for diction in storage:
        if diction["id"] == uid:
            return jsonify(diction), 200
    abort(404)
    # task = filter(lambda t: t['id'] == task_id, tasks)
    # if len(task) == 0:
    #     abort(404)
    # return jsonify({'task': task[0]})


# Добавить новый товар
@app.post('/api/v1/products/')
def add_product():
    # получить тело запроса можно с помощью модуля request payload = request.json()
    product = {
        'id': uuid4().hex,
        'title': request.json['title'],
        'category': request.json.get('category', "")
    }
    storage.append(product)
    # должны вернуть созданный у нас объект
    return jsonify(product), 200

# Обновить данные продукта
@app.put('/api/v1/products/<string:uid>')
def update_product(uid):
    for diction in storage:
        if diction["id"] == uid:
            diction['title'] = request.json.get('title', diction['title'])
            diction['category'] = request.json.get('category', diction['category'])
    # должны вернуть измененный объект
    return diction, 200

# Удалить показатель
@app.delete('/api/v1/products/<string:uid>')
def delete_product(uid):
    for diction in storage:
        if diction["id"] == uid:
            storage.remove(diction)
    # ничего не возвращаем, 204 - NO CONTENT
    return {}, 204
