import logging

from sqlalchemy.exc import IntegrityError

from backend.db import db_session
from backend.errors import ConflictError
from backend.models import User

logger = logging.getLogger(__name__)


class UserStorage():
    def add(self, tgid: int, username: str) -> User:
        add_user = User(tgid=tgid, username=username)
        db_session.add(add_user)
        try:
            db_session.commit()
        except IntegrityError:
            logging.exception('Can not add user')
            raise ConflictError(entity='users', method='add')
        return add_user
