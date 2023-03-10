from sqlalchemy import select

from app.core.db import session
from app.crud.base import CRUDBase
from app.models.organization import Organization


class CRUDOrganization(CRUDBase):
    def get_first(self):
        db_obj = self.session.execute(select(self.model))
        return db_obj.scalars().first()


organization_crud = CRUDOrganization(Organization, session)
