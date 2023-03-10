from sqlalchemy import select

from app.core.db import session
from app.crud.base import CRUDBase
from app.models.document import Document


class CRUDDocument(CRUDBase):
    def get_child(self, obj_id):
        db_obj = self.session.execute(
            select(self.model).where(
                self.model.parent_id == obj_id
            ).order_by(self.model.id)
        )
        return db_obj.scalars().all()

    def get_list_non_children(self):
        db_objs = self.session.execute(
            select(self.model).where(
                self.model.parent_id == None  # noqa
            ).order_by(self.model.id))
        return db_objs.scalars().all()


document_crud = CRUDDocument(Document, session)
