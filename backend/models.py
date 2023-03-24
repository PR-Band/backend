from sqlalchemy import Column, Integer, String

from backend.db import Base, engine


class Product(Base):

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)

    def __repr__(self):
        return f'products {self.id}, {self.title}'


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
