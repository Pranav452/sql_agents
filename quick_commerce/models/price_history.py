"""Price history model for Quick Commerce"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from .base import Base


class PriceHistory(Base):
    __tablename__ = 'price_histories'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    platform_id = Column(Integer, ForeignKey('platforms.id'))
    price = Column(Float, nullable=False)
    mrp = Column(Float)
    discount_percentage = Column(Float, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="price_histories")
    platform = relationship("Platform", back_populates="price_histories")
    
    # Indexes
    __table_args__ = (
        Index('idx_price_product_platform', 'product_id', 'platform_id'),
        Index('idx_price_timestamp', 'timestamp'),
    ) 