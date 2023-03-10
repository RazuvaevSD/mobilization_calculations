from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import Base


class Amount(Base):
    """Расчет ОБАС для выполнения мероприятий по мобилизации."""
    __tablename__ = 'amount'
    id = Column(Integer, primary_key=True)
    data_type = Column(String(50), doc='Тип записи. total или detail')
    document_id = Column(Integer, ForeignKey('documents.id'),
                         doc='ИД документа.')
    name = Column(String(450), doc='Наименование')
    type_expenses = Column(String(3),
                           doc='Вид расходов (группа, подгруппа, элемент).')
    amounts_transfer = Column(String, doc='ОБАС на план перевода.')
    amount_economy = Column(String, doc='ОБАС на план экономики.')
    total = Column(String, doc='Всего (сумма)')
    document = relationship('Document', back_populates='amount',
                            doc='Ссылка на документ.')
