from typing import Any

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

    def delete(self, uid: int):
        product_delete = Product.query.get(uid)
        db_session.delete(product_delete)
        db_session.commit()
