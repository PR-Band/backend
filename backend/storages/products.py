from sqlalchemy.exc import IntegrityError

from backend.db import db_session
from backend.errors import ConflictError, NotfoundError
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
        product_uid = Product.query.get(uid)
        if not product_uid:
            raise NotfoundError(entity='product', method='get_by_id')
        return product_uid

    def update(self, uid: int, title: str) -> Product:
        product_update = Product.query.get(uid)
        if not product_update:
            raise NotfoundError(entity='product', method='update')
        product_update.title = title
        try:
            db_session.commit()
        except IntegrityError:
            raise ConflictError(entity='products', method='add')
        return product_update

    def delete(self, uid: int):
        product_delete = Product.query.get(uid)
        if not product_delete:
            raise NotfoundError(entity='product', method='delete')
        db_session.delete(product_delete)
        db_session.commit()
