from http import HTTPStatus

from flask import Blueprint, abort, jsonify, request

from backend import schemas
from backend.storages.schedule_template import STStorage

view = Blueprint('schedule_templates', __name__)

storage = STStorage()


@view.post('/')
def add_schedule_templates():
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST)
    payload['id'] = -1
    new_schedule_template = schemas.ScheduleTemplate(**payload)
    #TODO: Слоты по 15 мин, не включая последний
    schedule_template = storage.add(
        new_schedule_template.product_id,
        new_schedule_template.day,
        new_schedule_template.start_slot,
        new_schedule_template.end_slot,
    )
    return jsonify(schedule_template.dict()), 200
