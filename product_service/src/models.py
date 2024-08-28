"""
This module contains the SQLAlchemy model for the product.
"""

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):
    """
    Represents a product.

    Attributes:
        id (int): The unique identifier of the product.
        name (str): The name of the product.
        description (str): The description of the product.
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
