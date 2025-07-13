"""Query Cache Manager for Quick Commerce"""

import hashlib
import logging
from datetime import datetime, timedelta
from typing import Optional
from ..models import QueryCache
from .manager import DatabaseManager

logger = logging.getLogger(__name__)

class QueryCacheManager:
    """Manages query result caching"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.cache_ttl = self.db_manager.config.CACHE_TTL
    
    def get_cache_key(self, query: str) -> str:
        """Generate cache key for query"""
        return hashlib.md5(query.encode()).hexdigest()
    
    def get_cached_result(self, query: str) -> Optional[str]:
        """Get cached result for query"""
        cache_key = self.get_cache_key(query)
        session = self.db_manager.get_session()
        
        try:
            cached = session.query(QueryCache).filter(
                QueryCache.query_hash == cache_key,
                QueryCache.expires_at > datetime.utcnow()
            ).first()
            
            if cached:
                # Increment hit count
                session.query(QueryCache).filter(
                    QueryCache.id == cached.id
                ).update({'hit_count': QueryCache.hit_count + 1})
                session.commit()
                return str(cached.result_data)
            
        except Exception as e:
            logger.error(f"Error getting cached result: {e}")
            session.rollback()
        finally:
            session.close()
        
        return None
    
    def cache_result(self, query: str, result: str):
        """Cache query result"""
        cache_key = self.get_cache_key(query)
        session = self.db_manager.get_session()
        
        try:
            # Remove old cache entry if exists
            session.query(QueryCache).filter(
                QueryCache.query_hash == cache_key
            ).delete()
            
            # Create new cache entry
            cache_entry = QueryCache(
                query_hash=cache_key,
                query_text=query,
                result_data=result,
                expires_at=datetime.utcnow() + timedelta(seconds=self.cache_ttl)
            )
            session.add(cache_entry)
            session.commit()
            
        except Exception as e:
            logger.error(f"Error caching result: {e}")
            session.rollback()
        finally:
            session.close()
    
    def clear_expired_cache(self):
        """Clear expired cache entries"""
        session = self.db_manager.get_session()
        
        try:
            expired_count = session.query(QueryCache).filter(
                QueryCache.expires_at <= datetime.utcnow()
            ).delete()
            
            session.commit()
            logger.info(f"Cleared {expired_count} expired cache entries")
            
        except Exception as e:
            logger.error(f"Error clearing expired cache: {e}")
            session.rollback()
        finally:
            session.close() 