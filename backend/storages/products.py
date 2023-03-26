from uuid import uuid4


class ProductsStorage:

    def __init__(self, products) -> None:
        self.storage = {product['id']: product for product in products}

    def get_all(self):
        return list(self.storage.values())

    def get_by_id(self, uid):
        return self.storage.get(uid)

    def add(self, new_product):
        new_uid = uuid4().hex
        new_product['id'] = new_uid
        self.storage[new_uid] = new_product
        # должны вернуть созданный у нас объект
        return new_product

    def update(self, payload, uid):
        old_product = self.storage.get(uid)
        if not old_product:
            return None
        old_product.update(payload)
        return payload

    def delete(self, uid):
        if uid not in self.storage:
            return False
        self.storage.pop(uid)
        return True

