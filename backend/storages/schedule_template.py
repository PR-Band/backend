import logging
from sqlalchemy.exc import IntegrityError
from backend.db import db_session
from backend.models import ScheduleTemplate
from backend.errors import ConflictError

logger = logging.getLogger(__name__)


class STStorage:

    def add(self, product_id: int, day: str, slot: str) -> ScheduleTemplate:
        add_schedule_template = ScheduleTemplate(product_id=product_id, day=day, slot=slot)
        db_session.add(add_schedule_template)
        try:
            db_session.commit()
        except IntegrityError:
            logger.exception('Can not add schedule_template')
            raise ConflictError(entity='schedule_template', method='add')
        return add_schedule_template


    # def add(self, title: str) -> Category:
    #     add_project = Category(title=title)
    #     db_session.add(add_project)
    #     try:
    #         db_session.commit()
    #     except IntegrityError:
    #         raise ConflictError(entity='categories', method='add')
    #     return add_project
