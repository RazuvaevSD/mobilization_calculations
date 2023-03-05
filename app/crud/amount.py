from app.crud.base import CRUDBase
from app.models.amount import Amount


class CRUDAmount(CRUDBase):
    pass


amount_crud = CRUDAmount(Amount)
