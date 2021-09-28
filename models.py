from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from database import Base


class Menu(Base):
    __tablename__ = 'menu'

    name = Column(String, primary_key=True, unique=True, index=True)
    description = Column(String)
    created = Column(DateTime)
    updated = Column(DateTime)    

    dishes = relationship("Dish", back_populates="owner")


class Dish(Base):
    __tablename__ = 'dish'

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String, index=True)
    description = Column(String)
    time_to_get_ready = Column(Integer)
    price = Column(Float)
    is_vgetarian = Column(Boolean)
    created = Column(DateTime)
    updated = Column(DateTime)
    owner_id = Column(String, ForeignKey("menu.name"), nullable=False)

    owner = relationship("Menu", back_populates="dishes")