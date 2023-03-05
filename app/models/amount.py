from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from app.core.db import Base


class Amount(Base):
    """Расчет ОБАС для выполнения мероприятий по мобилизации."""
    __tablename__ = 'amount'
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('documents.id'),
                         doc='ИД документа.')
    type_expenses = Column(Integer,
                           doc='Вид расходов (группа, элемент).')
    amounts_ba_to_wars = Column(Numeric,
                                doc='ОБАС на работу во время войны.')
    amount_ba_to_mob_tasks = Column(Numeric,
                                    doc='ОБАС на выполнение задач '
                                        'по мобилизации.')
    total = Column(Numeric, doc='Всего (сумма)')
    document = relationship('Document', back_populates='amount',
                            doc='Ссылка на документ.')
