"""Database Manager for Quick Commerce"""

import logging
import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from ..models import Base
from ..config import get_config

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Database connection and session management"""
    
    def __init__(self, config=None):
        self.config = config or get_config()
        self.engine = create_engine(
            self.config.DATABASE_URL,
            poolclass=StaticPool,
            pool_pre_ping=True,
            echo=False
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.cache = {}
        self.cache_lock = threading.Lock()
        
    def create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)
        logger.info("Database tables created successfully")
    
    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()
    
    def close(self):
        """Close database connections"""
        self.engine.dispose()
        logger.info("Database connections closed") 