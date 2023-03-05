from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import Base


class DocumentType(Base):
    """Тип документа."""
    __tablename__ = 'documents_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False,
                  doc='Наименование типа документа.')
    documents = relationship('Document', back_populates="type")
