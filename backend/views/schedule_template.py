
from http import HTTPStatus

from flask import Blueprint, abort, jsonify, request

from backend import models, schemas
from backend.storages.schedule_template import STStorage

view = Blueprint('schedule_templates', __name__)

storage = STStorage()


def split_time(time: str) -> tuple[int, int]:
    parts = time.split(':')
    return int(parts[0]), int(parts[1])


LAST_SLOT_MINUTES = 45
SLOT_INTERVAL = 15


def split_slots(start_slot: str, end_slot: str) -> list[str]:
    """Возвращает список слотов в указанном диапазоне, с шагом в 15 минут."""
    hh_start, mm_start = split_time(start_slot)
    hh_end, mm_end = split_time(end_slot)
    slots = []
    slots.append(start_slot)
    while hh_start != hh_end or mm_start != mm_end:
        if mm_start < LAST_SLOT_MINUTES:
            mm_start += SLOT_INTERVAL
        else:
            hh_start += 1
            mm_start = 0
        slots.append(f'{hh_start:02}:{mm_start:02}')
    slots.pop()
    return slots


def add_slots(new_schedule_template: schemas.ScheduleTemplate) -> list[models.ScheduleTemplate]:
    slots = split_slots(
        new_schedule_template.start_slot,
        new_schedule_template.end_slot,
    )
    new_slots = []
    for slot in slots:
        schedule_template = storage.add(
            new_schedule_template.product_id,
            new_schedule_template.day,
            slot,
        )
        new_slots.append(schedule_template)
    return new_slots


@view.post('/')
def add_schedule_templates():
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST)
    payload['id'] = -1
    schedule_template = schemas.ScheduleTemplate(**payload)
    slots = add_slots(schedule_template)
    response = [
        {
            'product_id': slot.product_id,
            'day': slot.day,
            'slot': slot.slot,
        }
        for slot in slots
    ]
    return jsonify(response), 200


@view.get('/')
def get_all_schedule_templates():
    slots = storage.get_all()
    all_slots = [
        schemas.ScheduleTemplate.from_orm(slot).dict()
        for slot in slots
    ]
    return jsonify(all_slots), 200


@view.get('/<string:day>')
def get_slots_by_day():
    # day = '2023-04-05'
    # date_dt = datetime.strptime(day, '%Y-%m-%d')
    # date_dt.strftime('%a')
    args = request.args
    args_day = args.get('day')
    if args_day:
        slots = storage.get_by_day(args_day.get('day'))
        new_slots = [
            schemas.ScheduleTemplate.from_orm(slot).dict()
            for slot in slots
        ]
    return jsonify(new_slots), 200
