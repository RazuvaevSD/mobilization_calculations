from app.crud.base import CRUDBase
from app.models.document import Document


class CRUDAmount(CRUDBase):
    pass


document_crud = CRUDAmount(Document)
