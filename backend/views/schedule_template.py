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
    schedule_template = storage.add(
        new_schedule_template.product_id,
        new_schedule_template.day,
        new_schedule_template.slot,
    )
    return jsonify(schemas.ScheduleTemplate.from_orm(schedule_template).dict()), 200



# @view.post('/')
# def add_user():
#     payload = request.json
#     if not payload:
#         abort(HTTPStatus.BAD_REQUEST)
#     payload['id'] = -1
#     new_user = schemas.User(**payload)
#     user = storage.add(new_user.tgid, new_user.username)
#     return jsonify(schemas.User.from_orm(user).dict()), 200
