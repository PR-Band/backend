from sqlalchemy import Column, Integer, String

from backend.db import Base, engine


class Salary(Base):

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    title = Column(String)

    def __repr__(self):
        return f'Salary {self.id}, {self.name}, {self.company}'


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
