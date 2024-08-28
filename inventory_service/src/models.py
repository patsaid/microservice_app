"""
This module contains the SQLAlchemy model for the inventory item.
"""

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Inventory(Base):
    """
    Represents an inventory item.

    Attributes:
        id (int): The unique identifier of the inventory item.
        product_id (int): The identifier of the associated product.
        quantity (int): The quantity of the inventory item.
    """

    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)
    quantity = Column(Integer)
