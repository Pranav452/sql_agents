"""Sample Data Populator for Quick Commerce"""

import random
import logging
from datetime import datetime, timedelta
from ..models import (
    Platform, Category, Brand, Product, 
    PriceHistory, Inventory, Discount
)
from .manager import DatabaseManager

logger = logging.getLogger(__name__)

class SampleDataPopulator:
    """Populates database with sample data"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.config = db_manager.config
    
    def populate_all(self):
        """Populate all sample data"""
        session = self.db_manager.get_session()
        
        try:
            self._create_platforms(session)
            self._create_categories(session)
            self._create_brands(session)
            session.commit()
            
            self._create_products(session)
            session.commit()
            
            self._generate_price_data(session)
            session.commit()
            
            logger.info("Sample data populated successfully")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error populating sample data: {e}")
            raise
        finally:
            session.close()
    
    def _create_platforms(self, session):
        """Create platform data"""
        platforms = [
            Platform(name="blinkit", display_name="Blinkit"),
            Platform(name="zepto", display_name="Zepto"),
            Platform(name="instamart", display_name="Swiggy Instamart"),
            Platform(name="bigbasket", display_name="BigBasket Now"),
            Platform(name="dunzo", display_name="Dunzo"),
        ]
        
        for platform in platforms:
            session.merge(platform)
    
    def _create_categories(self, session):
        """Create category data"""
        categories = [
            Category(name="Vegetables", level=0),
            Category(name="Fruits", level=0),
            Category(name="Dairy", level=0),
            Category(name="Grocery", level=0),
            Category(name="Snacks", level=0),
        ]
        
        for category in categories:
            session.merge(category)
    
    def _create_brands(self, session):
        """Create brand data"""
        brands = [
            Brand(name="Amul"),
            Brand(name="Tata"),
            Brand(name="Nestle"),
            Brand(name="Britannia"),
            Brand(name="Haldiram"),
        ]
        
        for brand in brands:
            session.merge(brand)
    
    def _create_products(self, session):
        """Create product data"""
        products_data = self.config.SAMPLE_DATA_PRODUCTS
        
        for platform in range(1, 6):  # 5 platforms
            for i, (name, brand_id, category_id, unit, quantity) in enumerate(products_data):
                product = Product(
                    name=name,
                    brand_id=brand_id,
                    category_id=category_id,
                    platform_id=platform,
                    sku=f"SKU_{platform}_{i+1}",
                    unit=unit,
                    quantity=quantity
                )
                session.add(product)
    
    def _generate_price_data(self, session):
        """Generate realistic price data for products"""
        products = session.query(Product).all()
        base_prices = self.config.BASE_PRICES
        platform_multipliers = self.config.PLATFORM_MULTIPLIERS
        
        for product in products:
            base_price = base_prices.get(product.name, 50)
            
            # Get platform multiplier
            multiplier = platform_multipliers.get(product.platform_id, 1.0)
            
            # Add some randomness
            variation = random.uniform(0.9, 1.1)
            final_price = base_price * multiplier * variation
            
            # Generate MRP (slightly higher)
            mrp = final_price * random.uniform(1.1, 1.3)
            
            # Calculate discount
            discount_pct = ((mrp - final_price) / mrp) * 100
            
            # Create price history
            price_history = PriceHistory(
                product_id=product.id,
                platform_id=product.platform_id,
                price=round(final_price, 2),
                mrp=round(mrp, 2),
                discount_percentage=round(discount_pct, 2),
                timestamp=datetime.utcnow()
            )
            session.add(price_history)
            
            # Create inventory
            inventory = Inventory(
                product_id=product.id,
                platform_id=product.platform_id,
                quantity_available=random.randint(50, 200),
                is_in_stock=True
            )
            session.add(inventory)
            
            # Create some discounts
            if random.random() < 0.3:  # 30% chance of additional discount
                discount = Discount(
                    product_id=product.id,
                    platform_id=product.platform_id,
                    discount_type="percentage",
                    discount_value=random.randint(10, 50),
                    start_date=datetime.utcnow(),
                    end_date=datetime.utcnow() + timedelta(days=7)
                )
                session.add(discount) 