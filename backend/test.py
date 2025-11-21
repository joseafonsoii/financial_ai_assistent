from agents.tools import get_stock_price, get_stock_history, financial_calculator, calculate_portfolio_metrics, get_market_news
import yfinance as yf

print("🧪 TESTE DETALHADO DAS FERRAMENTAS")

print("\n1. Testando get_stock_price...")
try:
    result = get_stock_price.invoke({"symbol": "AAPL"})
    print(f"✅ get_stock_price: {result}")
except Exception as e:
    print(f"❌ get_stock_price falhou: {e}")

print("\n2. Testando yfinance diretamente...")
try:
    stock = yf.Ticker("AAPL")
    info = stock.info
    print(f"✅ yfinance funciona:")
    print(f"   - Nome: {info.get('longName', 'N/A')}")
    print(f"   - Preço: {info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))}")
    print(f"   - Moeda: {info.get('currency', 'N/A')}")
except Exception as e:
    print(f"❌ yfinance falhou: {e}")

print("\n3. Testando get_stock_history...")
try:
    result = get_stock_history.invoke({"symbol": "AAPL", "period": "1mo"})
    print(f"✅ get_stock_history: {result}")
except Exception as e:
    print(f"❌ get_stock_history falhou: {e}")

print("\n4. Testando financial_calculator...")
try:
    result = financial_calculator.invoke({
        "operation": "compound_interest",
        "values": {"principal": 1000, "rate": 5, "years": 3}
    })
    print(f"✅ financial_calculator: {result}")
except Exception as e:
    print(f"❌ financial_calculator falhou: {e}")

print("\n5. Testando portfolio_metrics...")
try:
    result = calculate_portfolio_metrics.invoke({
        "investments": [
            {"symbol": "AAPL", "shares": 10, "purchase_price": 150},
            {"symbol": "MSFT", "shares": 5, "purchase_price": 300}
        ]
    })
    print(f"✅ calculate_portfolio_metrics: {result}")
except Exception as e:
    print(f"❌ calculate_portfolio_metrics falhou: {e}")

print("\n6. Testando market_news...")
try:
    result = get_market_news.invoke({"symbol": "AAPL"})
    print(f"✅ get_market_news: {result}")
except Exception as e:
    print(f"❌ get_market_news falhou: {e}")