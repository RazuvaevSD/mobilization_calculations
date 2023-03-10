from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import Base


class Document(Base):
    """Реквизиты документа."""
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    doc_type = Column(String(50), doc='Тип документа.')
    number = Column(String, doc='Экземпляр.')
    date = Column(String, doc='Дата документа.')
    org_name = Column(String(800),
                      doc='Наименование организации (в дательном падеже).')
    pos_head = Column(String(450), doc='Должность руководителя организации.')
    pos_coordinator = Column(String(450),
                             doc='Должность руководителя организации.')
    parent_id = Column(Integer, ForeignKey('documents.id'), nullable=True,
                       doc='ИД вышестоящего документа.')
    amount = relationship('Amount', back_populates='document',
                          doc='Ссылка на Расчет ОБАС на выполнение '
                              'мероприятий по мобилизации.')
    children = relationship('Document', doc='Ссылка на дочерние документы.',
                            back_populates='parent')
    parent = relationship("Document", remote_side=id,
                          doc='Ссылка на дочерние документы.')
