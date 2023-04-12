import logging

from sqlalchemy.exc import IntegrityError

from backend.db import db_session
from backend.errors import ConflictError, NotfoundError
from backend.models import Product, User

logger = logging.getLogger(__name__)


class Pgstorage:

    def add(self, title: str, category_id: int, user_id: int) -> Product:
        add_product = Product(
            title=title,
            category_id=category_id,
            user_id=user_id,
        )
        db_session.add(add_product)
        try:
            db_session.commit()
        except IntegrityError:
            logger.exception('Can not add product')
            raise ConflictError(entity='products', method='add')
        return add_product

    def get_all(self) -> list[Product]:
        return Product.query.all()

    def get_by_id(self, uid) -> Product:
        product_uid = Product.query.get(uid)
        if not product_uid:
            raise NotfoundError(entity='product', method='get_by_id')
        return product_uid

    def get_products(self, user_id) -> list[Product]:
        return Product.query.filter(Product.user_id == user_id).all()

    def update(self, uid: int, title: str, category_id: int) -> Product:
        product_update = Product.query.get(uid)
        if not product_update:
            raise NotfoundError(entity='product', method='update')
        product_update.title = title
        product_update.category_id = category_id
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
