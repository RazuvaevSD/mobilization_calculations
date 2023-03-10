from sqlalchemy import Integer, delete, func, select

from app.core.db import session
from app.crud.base import CRUDBase
from app.models.amount import Amount


class CRUDAmount(CRUDBase):

    def remove_by_doc(self, doc_id, data_type):
        self.session.execute(
            delete(self.model).where(
                self.model.document_id == doc_id,
                self.model.data_type == data_type)
        )
        self.session.commit()

    def get_by_type(self, obj_id, data_type):
        db_obj = self.session.execute(
            select(self.model).where(self.model.document_id == obj_id,
                                     self.model.data_type == data_type))
        return db_obj.scalars()

    def get_svod(self, list_id):
        db_objs = self.session.execute(
            select(
                self.model.name,
                self.model.type_expenses,
                func.sum(self.model.amounts_transfer.cast(Integer)).label(
                    'amount_transfer'),
                func.sum(self.model.amount_economy.cast(Integer)).label(
                    'amount_aconomy'),
                func.sum(self.model.total.cast(Integer).label('total'))
            ).where(
                self.model.data_type == 'detail',
                self.model.document_id.in_(list_id)
            ).group_by(
                self.model.name,
                self.model.type_expenses,
            ).order_by(
                self.model.type_expenses)
        )
        return db_objs.all()

    def get_svod_total(self, list_id):
        db_objs = self.session.execute(
            select(
                func.sum(self.model.amounts_transfer.cast(Integer)).label(
                    'amount_transfer'),
                func.sum(self.model.amount_economy.cast(Integer)).label(
                    'amount_economy'),
                func.sum(self.model.total.cast(Integer).label('total'))
            ).where(
                self.model.data_type == 'detail',
                self.model.document_id.in_(list_id))
        )
        return db_objs.first()


amount_crud = CRUDAmount(Amount, session)
