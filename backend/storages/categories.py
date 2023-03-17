from uuid import uuid4


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
