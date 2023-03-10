from sqlalchemy import Column, Integer, String

from app.core.db import Base


class Organization(Base):
    """Модель организации."""
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    pos_head = Column(String(400), nullable=False)
    pos_coordinator = Column(String(400), nullable=False)
