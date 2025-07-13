"""Web Application for Quick Commerce"""

import logging
import time
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

from .templates import WEB_INTERFACE_TEMPLATE
from ..database import DatabaseManager, SampleDataPopulator
from ..agents import AdvancedSQLAgent, PriceUpdater
from ..models import Platform, Product, Category, Brand, UserQuery

logger = logging.getLogger(__name__)

class QuickCommerceAPI:
    """Flask web application for Quick Commerce"""
    
    def __init__(self, config=None):
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Initialize components
        self.db_manager = DatabaseManager(config)
        self.sql_agent = AdvancedSQLAgent(self.db_manager)
        self.price_updater = PriceUpdater(self.db_manager)
        self.sample_data_populator = SampleDataPopulator(self.db_manager)
        
        # Rate limiting
        self.rate_limit = defaultdict(list)
        self.rate_limit_window = self.db_manager.config.RATE_LIMIT_WINDOW
        self.rate_limit_max = self.db_manager.config.RATE_LIMIT_MAX
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            return render_template_string(WEB_INTERFACE_TEMPLATE)
        
        @self.app.route('/api/query', methods=['POST'])
        def query():
            client_ip = request.remote_addr or "unknown"
            
            # Rate limiting
            if not self._check_rate_limit(client_ip):
                return jsonify({"error": "Rate limit exceeded"}), 429
            
            try:
                data = request.get_json()
                query_text = data.get('query', '')
                
                if not query_text:
                    return jsonify({"error": "Query is required"}), 400
                
                # Process query
                result = self.sql_agent.process_query(query_text)
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"Error processing query: {e}")
                return jsonify({"error": "Internal server error"}), 500
        
        @self.app.route('/api/platforms')
        def get_platforms():
            session = self.db_manager.get_session()
            try:
                platforms = session.query(Platform).filter(Platform.is_active == True).all()
                return jsonify([{
                    "id": p.id,
                    "name": p.name,
                    "display_name": p.display_name
                } for p in platforms])
            finally:
                session.close()
        
        @self.app.route('/api/stats')
        def get_stats():
            session = self.db_manager.get_session()
            try:
                # Get basic counts
                total_products = session.query(Product).count()
                total_platforms = session.query(Platform).filter(Platform.is_active == True).count()
                total_categories = session.query(Category).count()
                total_brands = session.query(Brand).count()
                
                # Get recent queries count
                recent_queries = session.query(UserQuery).filter(
                    UserQuery.timestamp >= datetime.utcnow() - timedelta(hours=24)
                ).count()
                
                # Get average query time
                avg_query_result = session.query(UserQuery).filter(
                    UserQuery.timestamp >= datetime.utcnow() - timedelta(hours=24),
                    UserQuery.execution_time.isnot(None)
                ).with_entities(UserQuery.execution_time).all()
                
                avg_query_time = 0.0
                if avg_query_result:
                    avg_query_time = sum(row[0] for row in avg_query_result) / len(avg_query_result)
                
                stats = {
                    "total_products": total_products,
                    "total_platforms": total_platforms,
                    "total_categories": total_categories,
                    "total_brands": total_brands,
                    "recent_queries": recent_queries,
                    "avg_query_time": avg_query_time
                }
                return jsonify(stats)
            finally:
                session.close()
        
        @self.app.route('/api/health')
        def health_check():
            return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})
    
    def _check_rate_limit(self, client_ip: str) -> bool:
        """Check if client is within rate limit"""
        current_time = time.time()
        
        # Clean old entries
        self.rate_limit[client_ip] = [
            timestamp for timestamp in self.rate_limit[client_ip]
            if current_time - timestamp < self.rate_limit_window
        ]
        
        # Check limit
        if len(self.rate_limit[client_ip]) >= self.rate_limit_max:
            return False
        
        # Add current request
        self.rate_limit[client_ip].append(current_time)
        return True
    
    def initialize(self):
        """Initialize the application"""
        logger.info("Initializing Quick Commerce Platform...")
        
        # Create database tables
        self.db_manager.create_tables()
        
        # Populate sample data
        self.sample_data_populator.populate_all()
        
        # Start price updater
        self.price_updater.start()
        
        logger.info("Platform initialized successfully")
    
    def run(self, host=None, port=None, debug=None):
        """Run the Flask application"""
        config = self.db_manager.config
        host = host or config.HOST
        port = port or config.PORT
        debug = debug or config.DEBUG
        
        self.initialize()
        self.app.run(host=host, port=port, debug=debug, threaded=True)
    
    def shutdown(self):
        """Shutdown the application"""
        logger.info("Shutting down Quick Commerce Platform...")
        self.price_updater.stop()
        self.db_manager.close()
        logger.info("Platform shutdown complete") 