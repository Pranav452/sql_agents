"""Product model for Quick Commerce"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from .base import Base


class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    brand_id = Column(Integer, ForeignKey('brands.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    platform_id = Column(Integer, ForeignKey('platforms.id'))
    sku = Column(String(100), unique=True, nullable=False)
    barcode = Column(String(50))
    unit = Column(String(20))  # kg, g, ml, pieces
    quantity = Column(Float)
    description = Column(Text)
    image_url = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    brand = relationship("Brand", back_populates="products")
    category = relationship("Category", back_populates="products")
    platform = relationship("Platform", back_populates="products")
    price_histories = relationship("PriceHistory", back_populates="product")
    inventory = relationship("Inventory", back_populates="product")
    discounts = relationship("Discount", back_populates="product")
    
    # Indexes
    __table_args__ = (
        Index('idx_product_platform', 'platform_id'),
        Index('idx_product_category', 'category_id'),
        Index('idx_product_brand', 'brand_id'),
        Index('idx_product_sku', 'sku'),
    ) 