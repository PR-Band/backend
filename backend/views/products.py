import locale
import logging
from datetime import date, datetime
from http import HTTPStatus

from flask import Blueprint, abort, jsonify, request

from backend import schemas
from backend.storages.products import Pgstorage
from backend.storages.schedule_template import STStorage
from backend.storages.slots import SlotStorage

view = Blueprint('products', __name__)


pgstorage = Pgstorage()
storage = STStorage()
slot_storage = SlotStorage()


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
    product = pgstorage.add(
        new_product.title,
        new_product.category_id,
        new_product.user_id,
    )
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


logger = logging.getLogger(__name__)

locale.setlocale(locale.LC_ALL, 'russian')


def date_day(day: date):
    # Получает день недели из конкретной даты
    logging.basicConfig(level=logging.INFO)
    logger.info(day.strftime('%a'))
    return day.strftime('%a')


def get_slot_time(day: date, slot: str) -> datetime:
    time_slot = datetime.strptime(slot, '%H:%M').time()
    return datetime.combine(day, time_slot)


@view.post('/<int:product_id>/slots/')
def add_slots(product_id: int):
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST)
    payload['id'] = -1
    slot_with_date = schemas.SlotsEntrance(**payload)
    day = date_day(slot_with_date.day)
    slots = storage.get_by_day(day, product_id)

    for slot in slots:
        slot_time = get_slot_time(slot_with_date.day, slot.slot)
        slot_storage.add(product_id, slot_time)
    response = [
        {
            'product_id': new_slot.product_id,
            'day': new_slot.day,
            'slot': new_slot.slot,
        }for new_slot in slots
    ]
    return jsonify(response), 204
