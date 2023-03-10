from sqlalchemy import select


class CRUDBase():

    def __init__(self, model, session):
        self.model = model
        self.session = session

    def get(self, obj_id: int):
        db_obj = self.session.execute(
            select(self.model).where(self.model.id == obj_id))
        return db_obj.scalars().first()

    def get_list(self):
        db_objs = self.session.execute(
            select(self.model).order_by(self.model.id))
        return db_objs.scalars().all()

    def create(self, obj_in):
        obj_in_data = obj_in
        db_obj = self.model(**obj_in_data)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def update(self, db_obj, obj_in):
        for field in obj_in:
            setattr(db_obj, field, obj_in[field])
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def remove(self, db_obj):
        self.session.delete(db_obj)
        self.session.commit()
        return db_obj
