"""Advanced SQL Agent for Quick Commerce"""

import json
import time
import logging
from typing import Dict, Any, Optional
from sqlalchemy.sql import text
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase

from .sql_llm import SQLGeneratorLLM
from ..database import DatabaseManager, QueryCacheManager
from ..models import UserQuery

logger = logging.getLogger(__name__)

class AdvancedSQLAgent:
    """Advanced SQL agent for natural language to SQL conversion"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.cache_manager = QueryCacheManager(db_manager)
        self.llm = SQLGeneratorLLM()
        
        # Initialize LangChain SQL database
        self.sql_db = SQLDatabase(engine=db_manager.engine)
        
        # Create SQL toolkit
        self.toolkit = SQLDatabaseToolkit(db=self.sql_db, llm=self.llm)
        
        # Create agent
        self.agent = create_sql_agent(
            llm=self.llm,
            toolkit=self.toolkit,
            verbose=True,
            max_iterations=3
        )
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process natural language query and return results"""
        start_time = time.time()
        
        # Check cache first
        cached_result = self.cache_manager.get_cached_result(query)
        if cached_result:
            return {
                "query": query,
                "results": json.loads(cached_result),
                "execution_time": time.time() - start_time,
                "cached": True
            }
        
        try:
            # Generate SQL query
            sql_query = self.llm._call(query)
            
            # Execute query
            session = self.db_manager.get_session()
            result = session.execute(text(sql_query)).fetchall()
            
            # Format results
            formatted_results = []
            for row in result:
                formatted_results.append({
                    "name": row[0],
                    "platform": row[1],
                    "price": row[2],
                    "discount": row[3] if len(row) > 3 else 0
                })
            
            execution_time = time.time() - start_time
            
            # Cache result
            result_json = json.dumps(formatted_results)
            self.cache_manager.cache_result(query, result_json)
            
            # Log query
            self._log_query(query, sql_query, execution_time, len(formatted_results), True)
            
            return {
                "query": query,
                "sql": sql_query,
                "results": formatted_results,
                "execution_time": execution_time,
                "cached": False
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            self._log_query(query, "", execution_time, 0, False, str(e))
            
            return {
                "query": query,
                "error": str(e),
                "execution_time": execution_time,
                "cached": False
            }
    
    def _log_query(self, query: str, sql: str, execution_time: float, 
                   result_count: int, success: bool, error: Optional[str] = None):
        """Log query execution details"""
        session = self.db_manager.get_session()
        
        try:
            log_entry = UserQuery(
                query_text=query,
                generated_sql=sql,
                execution_time=execution_time,
                result_count=result_count,
                is_successful=success,
                error_message=error
            )
            session.add(log_entry)
            session.commit()
            
        except Exception as e:
            logger.error(f"Error logging query: {e}")
            session.rollback()
        finally:
            session.close() 