from uuid import uuid4

from sqlalchemy.exc import IntegrityError

from backend.db import db_session
from backend.errors import ConflictError, NotfoundError
from backend.models import Category


class PgstorageCategory:

    def add(self, title: str) -> Category:
        add_project = Category(title=title)
        db_session.add(add_project)
        try:
            db_session.commit()
        except IntegrityError:
            raise ConflictError(entity='categories', method='add')
        return add_project

    # TODO: добавить not_found error
    def get_all(self) -> list[Category]:
        category = Category.query.all()
        if not category:
            raise NotfoundError(entity='categories', method='get_all')
        return category

    def get_by_id(self, uid) -> Category:
        category_uid = Category.query.get(uid)
        if not category_uid:
            raise NotfoundError(entity='categories', method='get_by_id')
        return category_uid

    # TODO: добавить conflicterror, notfound_error
    def update(self, uid: int, title: str) -> Category:
        category_update = Category.query.get(uid)
        if not category_update:
            raise NotfoundError(entity='categories', method='update')
        category_update.title = title
        try:
            db_session.commit()
        except IntegrityError:
            raise ConflictError(entity='categories', method='update')
        return category_update

    # TODO: добавить not_FOUND
    def delete(self, uid: int) -> bool:
        category_delete = Category.query.get(uid)
        if not category_delete:
            raise NotfoundError(entity='categories', method='update')

        db_session.delete(category_delete)
        db_session.commit()
        return True


class CategoryStorage:

    def __init__(self, categories) -> None:

        self.storage = {category['id']: category for category in categories}

    def get_all(self):
        return list(self.storage.values())

    def get_by_id(self, uid: str):
        self.category = self.storage.get(uid)
        return self.category

    def add(self, category):
        category['id'] = uuid4().hex
        self.storage[category['id']] = category
        return category

    def update(self, uid: str, new_category):
        old_category = self.storage.get(uid)
        if not old_category:
            return None

        old_category.update(new_category)
        return old_category

    def delete(self, uid: str) -> bool:
        if uid not in self.storage:
            return False

        self.storage.pop(uid)
        return True
