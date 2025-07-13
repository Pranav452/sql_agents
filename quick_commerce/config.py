"""Configuration settings for Quick Commerce platform"""

import os
from typing import Dict, Any, Optional

class Config:
    """Base configuration class"""
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///quick_commerce.db')
    
    # Cache
    CACHE_TTL = int(os.getenv('CACHE_TTL', '300'))  # 5 minutes
    
    # Rate limiting
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '60'))  # seconds
    RATE_LIMIT_MAX = int(os.getenv('RATE_LIMIT_MAX', '100'))  # requests per window
    
    # Price update frequency
    PRICE_UPDATE_INTERVAL = int(os.getenv('PRICE_UPDATE_INTERVAL', '30'))  # seconds
    
    # Web server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '5001'))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Sample data
    SAMPLE_DATA_PRODUCTS = [
        ("Onion", 1, 1, "kg", 1.0),
        ("Apple", 2, 2, "kg", 1.0),
        ("Milk", 3, 1, "ltr", 1.0),
        ("Bread", 4, 4, "pieces", 1.0),
        ("Rice", 4, 2, "kg", 1.0),
        ("Oil", 4, 3, "ltr", 1.0),
        ("Sugar", 4, 4, "kg", 1.0),
        ("Salt", 4, 5, "kg", 1.0),
    ]
    
    BASE_PRICES = {
        "Onion": 40, "Apple": 150, "Milk": 55, "Bread": 25,
        "Rice": 80, "Oil": 120, "Sugar": 50, "Salt": 20
    }
    
    PLATFORM_MULTIPLIERS = {
        1: 1.0,    # blinkit
        2: 0.95,   # zepto
        3: 1.05,   # instamart
        4: 0.98,   # bigbasket
        5: 1.02,   # dunzo
    }


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    DATABASE_URL = 'sqlite:///quick_commerce_dev.db'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///quick_commerce_prod.db')
    CACHE_TTL = 600  # 10 minutes in production


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    DATABASE_URL = 'sqlite:///quick_commerce_test.db'
    CACHE_TTL = 60  # 1 minute for testing


# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(environment: Optional[str] = None) -> Config:
    """Get configuration for the specified environment"""
    if environment is None:
        environment = os.getenv('ENVIRONMENT', 'default') or 'default'
    
    return config_map.get(environment, DevelopmentConfig) 