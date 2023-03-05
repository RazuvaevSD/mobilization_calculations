from app.crud.base import CRUDBase
from app.models.document_type import DocumentType


class CRUDAmount(CRUDBase):
    pass


document_type_crud = CRUDAmount(DocumentType)
