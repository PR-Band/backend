from typing import Any
from uuid import uuid4

from sqlalchemy.exc import IntegrityError

from backend.db import db_session
from backend.errors import ConflictError
from backend.models import Product


class Pgstorage:

    def add(self, title: str) -> Product:
        add_product = Product(title=title)
        db_session.add(add_product)
        try:
            db_session.commit()
        except IntegrityError:
            raise ConflictError(entity='products', method='add')
        return add_product

    def get_all(self) -> list[Product]:
        return Product.query.all()

    def get_by_id(self, uid) -> Product:
        return Product.query.get(uid)

    def update(self, payload: dict[str, Any], uid: int) -> Product:
        product_update = Product.query.get(uid)
        product_update.title = payload['title']
        db_session.commit()
        return product_update

    def delete(self, uid: int) -> None:
        product_delete = Product.query.get(uid)
        db_session.delete(product_delete)
        db_session.commit()


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
