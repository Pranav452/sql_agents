"""SQL Generator LLM for Quick Commerce"""

import re
from typing import Optional, List
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun


class SQLGeneratorLLM(LLM):
    """Custom LLM for generating SQL queries from natural language"""
    
    def __init__(self):
        super().__init__()
        self._query_templates = {
            'cheapest_product': """
                SELECT p.name, pl.name as platform, ph.price, ph.discount_percentage
                FROM products p
                JOIN price_histories ph ON p.id = ph.product_id
                JOIN platforms pl ON ph.platform_id = pl.id
                WHERE p.name LIKE '%{product}%' AND ph.timestamp >= datetime('now', '-1 hour')
                ORDER BY ph.price ASC
                LIMIT 10
            """,
            'discount_products': """
                SELECT p.name, pl.name as platform, ph.price, ph.discount_percentage
                FROM products p
                JOIN price_histories ph ON p.id = ph.product_id
                JOIN platforms pl ON ph.platform_id = pl.id
                WHERE ph.discount_percentage >= {discount} AND pl.name LIKE '%{platform}%'
                ORDER BY ph.discount_percentage DESC
                LIMIT 20
            """,
            'compare_prices': """
                SELECT p.name, pl.name as platform, ph.price, ph.discount_percentage
                FROM products p
                JOIN price_histories ph ON p.id = ph.product_id
                JOIN platforms pl ON ph.platform_id = pl.id
                JOIN categories c ON p.category_id = c.id
                WHERE c.name LIKE '%{category}%' 
                AND pl.name IN ({platforms})
                ORDER BY p.name, ph.price ASC
            """,
            'best_deals': """
                SELECT p.name, pl.name as platform, ph.price, ph.discount_percentage,
                       (ph.mrp - ph.price) as savings
                FROM products p
                JOIN price_histories ph ON p.id = ph.product_id
                JOIN platforms pl ON ph.platform_id = pl.id
                WHERE ph.price <= {budget} AND ph.discount_percentage > 0
                ORDER BY ph.discount_percentage DESC
                LIMIT 50
            """
        }
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None, 
              run_manager: Optional[CallbackManagerForLLMRun] = None) -> str:
        """Generate SQL query based on natural language prompt"""
        
        prompt_lower = prompt.lower()
        
        # Pattern matching for different query types
        if 'cheapest' in prompt_lower and any(word in prompt_lower for word in ['onion', 'apple', 'milk', 'bread']):
            product = self._extract_product(prompt_lower)
            return self._query_templates['cheapest_product'].format(product=product)
        
        elif 'discount' in prompt_lower and any(platform in prompt_lower for platform in ['blinkit', 'zepto', 'instamart']):
            discount = self._extract_discount(prompt_lower)
            platform = self._extract_platform(prompt_lower)
            return self._query_templates['discount_products'].format(discount=discount, platform=platform)
        
        elif 'compare' in prompt_lower and 'between' in prompt_lower:
            category = self._extract_category(prompt_lower)
            platforms = self._extract_platforms(prompt_lower)
            return self._query_templates['compare_prices'].format(category=category, platforms=platforms)
        
        elif 'best deals' in prompt_lower or 'grocery list' in prompt_lower:
            budget = self._extract_budget(prompt_lower)
            return self._query_templates['best_deals'].format(budget=budget)
        
        else:
            # Generic product search
            return f"""
                SELECT p.name, pl.name as platform, ph.price, ph.discount_percentage
                FROM products p
                JOIN price_histories ph ON p.id = ph.product_id
                JOIN platforms pl ON ph.platform_id = pl.id
                WHERE p.name LIKE '%{prompt}%'
                ORDER BY ph.price ASC
                LIMIT 10
            """
    
    def _extract_product(self, prompt: str) -> str:
        """Extract product name from prompt"""
        products = ['onion', 'apple', 'milk', 'bread', 'rice', 'oil', 'sugar', 'salt']
        for product in products:
            if product in prompt:
                return product
        return 'product'
    
    def _extract_discount(self, prompt: str) -> int:
        """Extract discount percentage from prompt"""
        match = re.search(r'(\d+)%', prompt)
        return int(match.group(1)) if match else 20
    
    def _extract_platform(self, prompt: str) -> str:
        """Extract platform name from prompt"""
        platforms = ['blinkit', 'zepto', 'instamart', 'bigbasket']
        for platform in platforms:
            if platform in prompt:
                return platform
        return 'blinkit'
    
    def _extract_category(self, prompt: str) -> str:
        """Extract category from prompt"""
        categories = ['fruit', 'vegetable', 'dairy', 'grocery', 'snacks']
        for category in categories:
            if category in prompt:
                return category
        return 'grocery'
    
    def _extract_platforms(self, prompt: str) -> str:
        """Extract multiple platforms from prompt"""
        platforms = []
        if 'zepto' in prompt:
            platforms.append("'zepto'")
        if 'instamart' in prompt:
            platforms.append("'instamart'")
        if 'blinkit' in prompt:
            platforms.append("'blinkit'")
        if 'bigbasket' in prompt:
            platforms.append("'bigbasket'")
        
        return ', '.join(platforms) if platforms else "'blinkit', 'zepto'"
    
    def _extract_budget(self, prompt: str) -> int:
        """Extract budget from prompt"""
        match = re.search(r'₹(\d+)', prompt)
        return int(match.group(1)) if match else 1000
    
    @property
    def _llm_type(self) -> str:
        return "sql_generator" 