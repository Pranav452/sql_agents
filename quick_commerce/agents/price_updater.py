"""Price Updater for Quick Commerce"""

import random
import time
import logging
import threading
from datetime import datetime
from sqlalchemy.sql import text
from ..database import DatabaseManager
from ..models import Product, PriceHistory

logger = logging.getLogger(__name__)

class PriceUpdater:
    """Real-time price updater for Quick Commerce"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.config = db_manager.config
        self.running = False
        self.update_thread = None
    
    def start(self):
        """Start price update thread"""
        self.running = True
        self.update_thread = threading.Thread(target=self._update_prices)
        self.update_thread.daemon = True
        self.update_thread.start()
        logger.info("Price updater started")
    
    def stop(self):
        """Stop price update thread"""
        self.running = False
        if self.update_thread:
            self.update_thread.join()
        logger.info("Price updater stopped")
    
    def _update_prices(self):
        """Background thread to update prices"""
        while self.running:
            try:
                self._simulate_price_updates()
                time.sleep(self.config.PRICE_UPDATE_INTERVAL)
            except Exception as e:
                logger.error(f"Error updating prices: {e}")
                time.sleep(60)  # Wait longer on error
    
    def _simulate_price_updates(self):
        """Simulate real-time price updates"""
        session = self.db_manager.get_session()
        
        try:
            # Get random products to update
            products = session.query(Product).order_by(text('RANDOM()')).limit(10).all()
            
            for product in products:
                # Get latest price
                latest_price = session.query(PriceHistory).filter(
                    PriceHistory.product_id == product.id,
                    PriceHistory.platform_id == product.platform_id
                ).order_by(PriceHistory.timestamp.desc()).first()
                
                if latest_price:
                    # Create price variation (±5%)
                    variation = random.uniform(0.95, 1.05)
                    new_price = float(latest_price.price) * variation
                    
                    # Update discount randomly
                    discount_change = random.uniform(-5, 5)
                    new_discount = max(0, min(50, float(latest_price.discount_percentage) + discount_change))
                    
                    # Create new price history entry
                    new_price_history = PriceHistory(
                        product_id=product.id,
                        platform_id=product.platform_id,
                        price=round(new_price, 2),
                        mrp=float(latest_price.mrp),
                        discount_percentage=round(new_discount, 2),
                        timestamp=datetime.utcnow()
                    )
                    session.add(new_price_history)
            
            session.commit()
            logger.info("Price updates completed")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error in price simulation: {e}")
        finally:
            session.close() 