from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import Base


class Organization(Base):
    """Модель организации."""
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    inn = Column(String(10), nullable=False)
    name = Column(String(250), nullable=False)
    position_head = Column(String(400), nullable=False)
    fio_head = Column(String(250), nullable=False)
    mob_position_head = Column(String(400), nullable=False)
    mob_fio_head = Column(String(250), nullable=False)
    documents = relationship('Document', back_populates='organization',
                             doc='Ссылка на документы.')
