"""Cache model for Quick Commerce"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from .base import Base


class QueryCache(Base):
    __tablename__ = 'query_cache'
    
    id = Column(Integer, primary_key=True)
    query_hash = Column(String(64), unique=True, nullable=False)
    query_text = Column(Text, nullable=False)
    result_data = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    hit_count = Column(Integer, default=0)
    
    # Indexes
    __table_args__ = (
        Index('idx_cache_hash', 'query_hash'),
        Index('idx_cache_expires', 'expires_at'),
    ) 