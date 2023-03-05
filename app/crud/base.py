from sqlalchemy import select


class CRUDBase():

    def __init__(self, model):
        self.model = model

    async def get(self,
                  obj_id: int,
                  session):
        db_obj = session.execute(
            select(self.model).where(self.model.id == obj_id))
        return db_obj.scalars().first()

    async def get_list(self, session):
        db_objs = session.execute(select(self.model))
        return db_objs.scalars().all()

    def create(self, obj_in, session):
        obj_in_data = obj_in
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    @staticmethod
    def update(db_obj, obj_in, session):
        for field in db_obj:
            if field in obj_in:
                setattr(db_obj, field, obj_in[field])
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    @staticmethod
    async def remove(db_obj, session,):
        session.delete(db_obj)
        session.commit()
        return db_obj
