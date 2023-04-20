from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from backend.db import Base, engine


class Category(Base):

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    products = relationship('Product', back_populates='category')

    def __repr__(self):
        return f'categories {self.id}, {self.title}'


class Product(Base):

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=False)
    category_id = Column(
        Integer,
        ForeignKey('categories.id', onupdate='RESTRICT', ondelete='RESTRICT'),
        nullable=False,
    )
    category = relationship('Category', back_populates='products')

    user_id = Column(
        Integer,
        ForeignKey('users.id', onupdate='RESTRICT', ondelete='RESTRICT'),
        nullable=False,
    )
    user = relationship('User', back_populates='products')

    schedule_templates = relationship('ScheduleTemplate', back_populates='product')

    slots = relationship('Slot', back_populates='product')

    def __repr__(self):
        return f'Product {self.id}, {self.title}, {self.category_id}'


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tgid = Column(Integer, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    products = relationship('Product', back_populates='user')

    def __repr__(self):
        return f'Users {self.id}, {self.tgid}, {self.username}'


class ScheduleTemplate(Base):
    __tablename__ = 'schedule_templates'
    __table_args__ = (UniqueConstraint('day', 'slot', name='schedule_templates_day_slot_uc'), )

    id = Column(Integer, primary_key=True)
    product_id = Column(
        Integer,
        ForeignKey('products.id', onupdate='RESTRICT', ondelete='RESTRICT'),
        nullable=False,
    )
    day = Column(String)
    slot = Column(String)

    product = relationship('Product', back_populates='schedule_templates')


class Slot(Base):
    __tablename__ = 'slots'

    id = Column(Integer, primary_key=True)
    product_id = Column(
        Integer,
        ForeignKey('products.id', onupdate='RESTRICT', ondelete='RESTRICT'),
        nullable=False,
    )
    slot = Column(DateTime)

    product = relationship('Product', back_populates='slots')


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
