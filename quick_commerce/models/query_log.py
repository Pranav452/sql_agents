"""User query model for Quick Commerce"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, Boolean, Text, DateTime, Index
from .base import Base


class UserQuery(Base):
    __tablename__ = 'user_queries'
    
    id = Column(Integer, primary_key=True)
    query_text = Column(Text, nullable=False)
    generated_sql = Column(Text)
    execution_time = Column(Float)
    result_count = Column(Integer)
    is_successful = Column(Boolean, default=True)
    error_message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index('idx_query_timestamp', 'timestamp'),
    ) 