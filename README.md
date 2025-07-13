# Quick Commerce Price Comparison Platform

A modular and scalable platform for comparing prices across multiple quick commerce platforms like Blinkit, Zepto, Instamart, BigBasket, and more.

## 🏗️ Project Structure

```
quick_commerce/
├── __init__.py                 # Package initialization
├── config.py                   # Configuration management
├── models/                     # Database models
│   ├── __init__.py
│   ├── base.py                 # SQLAlchemy base
│   ├── platform.py             # Platform model
│   ├── category.py             # Category model
│   ├── brand.py                # Brand model
│   ├── product.py              # Product model
│   ├── price_history.py        # Price history model
│   ├── inventory.py            # Inventory model
│   ├── discount.py             # Discount model
│   ├── query_log.py            # Query logging model
│   └── cache.py                # Cache model
├── database/                   # Database management
│   ├── __init__.py
│   ├── manager.py              # Database manager
│   ├── cache.py                # Cache manager
│   └── sample_data.py          # Sample data populator
├── agents/                     # AI agents and background services
│   ├── __init__.py
│   ├── sql_llm.py              # SQL generation LLM
│   ├── sql_agent.py            # SQL agent
│   └── price_updater.py        # Price update service
├── web/                        # Web interface
│   ├── __init__.py
│   ├── app.py                  # Flask application
│   └── templates.py            # HTML templates
├── utils/                      # Utility functions (future use)
│   └── __init__.py
└── monitoring/                 # Monitoring and metrics (future use)
    └── __init__.py

app.py                          # Main application entry point
requirements.txt                # Dependencies
README.md                       # This file
```

## 🚀 Quick Start

### 1. Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Set environment variables (optional):
```bash
export DATABASE_URL="sqlite:///quick_commerce.db"
export HOST="0.0.0.0"
export PORT="5001"
export DEBUG="True"
export ENVIRONMENT="development"
```

### 3. Run the Application

```bash
python app.py
```

### 4. Access the Platform

- **Web Interface**: http://localhost:5001
- **API Documentation**: http://localhost:5001/api/
- **Health Check**: http://localhost:5001/api/health

## 🎯 Key Features

### ✅ Modular Architecture
- **Separation of Concerns**: Each module has a specific responsibility
- **Maintainable Code**: Easy to understand and modify
- **Testable**: Individual components can be tested in isolation
- **Scalable**: Easy to add new features and platforms

### ✅ Database Management
- **SQLAlchemy ORM**: Type-safe database operations
- **Migration Support**: Easy schema changes
- **Connection Pooling**: Efficient database connections
- **Caching**: Query result caching for performance

### ✅ AI-Powered Query Processing
- **Natural Language**: "Which app has cheapest onions?"
- **SQL Generation**: Intelligent query conversion
- **Pattern Recognition**: Understands different query types
- **Caching**: Fast response times for repeated queries

### ✅ Real-time Price Updates
- **Background Processing**: Continuous price monitoring
- **Simulation**: Realistic price variations
- **Thread-safe**: Concurrent price updates
- **Configurable**: Customizable update intervals

### ✅ Web Interface
- **Responsive Design**: Mobile-friendly interface
- **Real-time Updates**: Live price comparisons
- **Interactive**: Click-to-query sample searches
- **Statistics**: Platform performance metrics

## 📊 API Endpoints

### Query Processing
```bash
POST /api/query
{
  "query": "Which app has cheapest onions right now?"
}
```

### Platform Information
```bash
GET /api/platforms
```

### Statistics
```bash
GET /api/stats
```

### Health Check
```bash
GET /api/health
```

## 🛠️ Development

### Adding New Models
1. Create new model in `quick_commerce/models/`
2. Add import to `quick_commerce/models/__init__.py`
3. Update database with new tables

### Adding New Agents
1. Create agent in `quick_commerce/agents/`
2. Add import to `quick_commerce/agents/__init__.py`
3. Integrate with main application

### Adding New Web Routes
1. Add routes to `quick_commerce/web/app.py`
2. Update templates if needed

### Environment Configuration
Create a `.env` file:
```
DATABASE_URL=sqlite:///quick_commerce.db
HOST=0.0.0.0
PORT=5001
DEBUG=True
ENVIRONMENT=development
CACHE_TTL=300
RATE_LIMIT_WINDOW=60
RATE_LIMIT_MAX=100
PRICE_UPDATE_INTERVAL=30
```

## 📈 Sample Queries

The platform understands natural language queries:

- **Price Comparison**: "Which app has cheapest onions right now?"
- **Discount Search**: "Show products with 30%+ discount on Blinkit"
- **Platform Comparison**: "Compare fruit prices between Zepto and Instamart"
- **Budget Shopping**: "Find best deals for ₹1000 grocery list"

## 🔧 Technical Details

### Database Schema
- **10+ interconnected tables** for comprehensive data modeling
- **Optimized indexes** for fast query performance
- **Relationship mapping** for complex queries
- **Timestamp tracking** for price history

### Performance Optimizations
- **Connection pooling** for database efficiency
- **Query result caching** with TTL
- **Background processing** for price updates
- **Rate limiting** for API protection

### Security Features
- **Input validation** for all API endpoints
- **Rate limiting** to prevent abuse
- **Error handling** with proper logging
- **SQL injection protection** via ORM

## 🎉 Acknowledgments

- Built with Flask, SQLAlchemy, and LangChain
- Inspired by the need for transparent price comparison
- Designed for scalability and maintainability 