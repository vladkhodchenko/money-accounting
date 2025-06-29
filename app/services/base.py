from database import session
from sqlalchemy import select, insert, delete, update


class BaseService:
    model = None

    @classmethod
    def find_by_id(cls, model_id: int):
        with session() as s:
            query = select(cls.model).filter_by(id=model_id)
            result = s.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    def find_one_or_none(cls, **filter_by):
        with session() as s:
            query = select(cls.model).filter_by(**filter_by)
            result = s.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    def find_all(cls, **filter_by):
        with session() as s:
            query = select(cls.model).filter_by(**filter_by)
            result = s.execute(query)
            return result.scalars().all()

    @classmethod
    def insert(cls, **values):
        with session() as s:
            query = insert(cls.model).values(**values)
            result = s.execute(query)
            s.commit()
            return result.inserted_primary_key[0] if result.inserted_primary_key else None
            
    @classmethod
    def delete(cls, item: str):
        with session() as s:
            s.delete(item)
            s.commit()
            return True

    @classmethod
    def find_name(cls, model_name:str):
        print(model_name)
        with session() as s:
            query = select(cls.model).filter_by(name=model_name)
            result = s.execute(query)
            return result.scalars().first()


    @classmethod
    def find_id(cls, model_id:str):
        with session() as s:
            query = select(cls.model).filter_by(id=model_id)
            result = s.execute(query)
            return result.scalars().one_or_none()
        

    @classmethod
    def update(cls, model_name: str, **values):
        with session() as s:
            query = update(cls.model).where(cls.model.name == model_name).values(**values)
            result = s.execute(query)
            return result.rowcount