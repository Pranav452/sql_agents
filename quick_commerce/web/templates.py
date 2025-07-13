"""HTML Templates for Quick Commerce Web Interface"""

WEB_INTERFACE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quick Commerce Price Comparison</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .query-section {
            padding: 40px;
            background: #f8f9fa;
        }
        
        .query-container {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .query-input {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        .query-input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .query-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .query-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .sample-queries {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .sample-query {
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 15px;
            cursor: pointer;
            transition: border-color 0.3s, transform 0.3s;
        }
        
        .sample-query:hover {
            border-color: #667eea;
            transform: translateY(-2px);
        }
        
        .sample-query h4 {
            color: #333;
            margin-bottom: 5px;
        }
        
        .sample-query p {
            color: #666;
            font-size: 0.9em;
        }
        
        .results-section {
            padding: 40px;
            background: white;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        
        .loading::after {
            content: "...";
            animation: loading 2s infinite;
        }
        
        @keyframes loading {
            0% { content: "..."; }
            33% { content: "..."; }
            66% { content: "..."; }
            100% { content: "..."; }
        }
        
        .error {
            background: #fee;
            color: #c33;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .query-info {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }
        
        .results-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }
        
        .result-card {
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .result-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }
        
        .product-name {
            font-size: 1.1em;
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
        }
        
        .platform-name {
            color: #667eea;
            font-weight: 500;
            margin-bottom: 10px;
        }
        
        .price {
            font-size: 1.5em;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 10px;
        }
        
        .discount {
            background: #48bb78;
            color: white;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
            display: inline-block;
        }
        
        .stats-section {
            padding: 40px;
            background: #f8f9fa;
            border-top: 1px solid #e9ecef;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
        
        .footer {
            background: #2d3748;
            color: white;
            text-align: center;
            padding: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Quick Commerce Price Comparison</h1>
            <p>Compare prices across Blinkit, Zepto, Instamart, BigBasket & more</p>
        </div>
        
        <div class="query-section">
            <div class="query-container">
                <input type="text" id="queryInput" class="query-input" 
                       placeholder="Ask me anything about prices... e.g., 'Which app has cheapest onions?'">
                <button onclick="executeQuery()" class="query-button">Search</button>
            </div>
            
            <div class="sample-queries">
                <div class="sample-query" onclick="setQuery('Which app has cheapest onions right now?')">
                    <h4>🧅 Cheapest Onions</h4>
                    <p>Find the best price for onions across all platforms</p>
                </div>
                <div class="sample-query" onclick="setQuery('Show products with 30%+ discount on Blinkit')">
                    <h4>🔥 Best Discounts</h4>
                    <p>Products with highest discounts on Blinkit</p>
                </div>
                <div class="sample-query" onclick="setQuery('Compare fruit prices between Zepto and Instamart')">
                    <h4>🍎 Price Comparison</h4>
                    <p>Compare fruit prices between different platforms</p>
                </div>
                <div class="sample-query" onclick="setQuery('Find best deals for ₹1000 grocery list')">
                    <h4>💰 Budget Shopping</h4>
                    <p>Best deals within your budget</p>
                </div>
            </div>
        </div>
        
        <div class="results-section">
            <div id="results"></div>
        </div>
        
        <div class="stats-section">
            <h2 style="text-align: center; margin-bottom: 30px; color: #333;">Platform Statistics</h2>
            <div class="stats-grid" id="stats"></div>
        </div>
        
        <div class="footer">
            <p>© 2025 Quick Commerce Platform - Real-time price comparison made easy</p>
        </div>
    </div>

    <script>
        function setQuery(query) {
            document.getElementById('queryInput').value = query;
        }
        
        function executeQuery() {
            const query = document.getElementById('queryInput').value;
            if (!query.trim()) return;
            
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '<div class="loading">Processing your query</div>';
            
            fetch('/api/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: query })
            })
            .then(response => response.json())
            .then(data => {
                displayResults(data);
            })
            .catch(error => {
                resultsDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
            });
        }
        
        function displayResults(data) {
            const resultsDiv = document.getElementById('results');
            
            if (data.error) {
                resultsDiv.innerHTML = `<div class="error">Error: ${data.error}</div>`;
                return;
            }
            
            let html = `
                <div class="query-info">
                    <strong>Query:</strong> ${data.query}<br>
                    <strong>Execution Time:</strong> ${data.execution_time.toFixed(3)}s<br>
                    <strong>Results:</strong> ${data.results.length} items
                    ${data.cached ? ' (cached)' : ''}
                </div>
            `;
            
            if (data.results.length === 0) {
                html += '<div class="error">No results found for your query.</div>';
            } else {
                html += '<div class="results-grid">';
                data.results.forEach(result => {
                    html += `
                        <div class="result-card">
                            <div class="product-name">${result.name}</div>
                            <div class="platform-name">${result.platform}</div>
                            <div class="price">₹${result.price}</div>
                            ${result.discount > 0 ? `<div class="discount">${result.discount.toFixed(1)}% OFF</div>` : ''}
                        </div>
                    `;
                });
                html += '</div>';
            }
            
            resultsDiv.innerHTML = html;
        }
        
        function loadStats() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    const statsDiv = document.getElementById('stats');
                    statsDiv.innerHTML = `
                        <div class="stat-card">
                            <div class="stat-value">${data.total_products}</div>
                            <div class="stat-label">Total Products</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${data.total_platforms}</div>
                            <div class="stat-label">Platforms</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${data.total_categories}</div>
                            <div class="stat-label">Categories</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${data.total_brands}</div>
                            <div class="stat-label">Brands</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${data.recent_queries}</div>
                            <div class="stat-label">24h Queries</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${data.avg_query_time.toFixed(3)}s</div>
                            <div class="stat-label">Avg Query Time</div>
                        </div>
                    `;
                })
                .catch(error => {
                    console.error('Error loading stats:', error);
                });
        }
        
        // Handle Enter key
        document.getElementById('queryInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                executeQuery();
            }
        });
        
        // Load stats on page load
        loadStats();
        
        // Refresh stats every 30 seconds
        setInterval(loadStats, 30000);
    </script>
</body>
</html>
""" 