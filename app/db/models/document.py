from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import Base


class Document(Base):
    """Реквизиты документа."""
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('documents_types.id'),
                     doc='ИД типа документа.')
    number = Column(Integer,
                    doc='Номер документа.')
    name = Column(String(450),
                  doc='Наименование документа.')
    date = Column(DateTime,
                  doc='Дата документа.')
    parent_id = Column(Integer, ForeignKey('documents.id'),
                       doc='ИД вышестоящего документа.')
    organization_id = Column(Integer, ForeignKey('organization.id'),
                             doc='ИД организации.')
    organization = relationship('Organization', back_populates='documents',
                                doc='Ссылка на организацию.')
    type = relationship('DocumentType', back_populates="documents",
                        doc='Ссылка на тип документа.')
    amount = relationship('Amount', back_populates='document',
                          doc='Ссылка на Расчет ОБАС на выполнение '
                              'мероприятий по мобилизации.')
    children = relationship('Document', doc='Ссылка на дочерние документы.',
                            back_populates='parent')
    parent = relationship("Document", remote_side=id,
                          doc='Ссылка на дочерние документы.')
