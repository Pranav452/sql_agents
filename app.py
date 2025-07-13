#!/usr/bin/env python3
"""
Quick Commerce Price Comparison Platform
Main application entry point
"""

import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from quick_commerce.web import QuickCommerceAPI
from quick_commerce.config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Main application entry point"""
    try:
        # Get configuration
        config = get_config()
        
        # Create and run the application
        app = QuickCommerceAPI(config)
        
        logger.info("Starting Quick Commerce Platform...")
        app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
        
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 