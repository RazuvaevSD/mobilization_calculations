from app.crud.base import CRUDBase
from app.models.organization import Organization


class CRUDAmount(CRUDBase):
    pass


organization_crud = CRUDAmount(Organization)
