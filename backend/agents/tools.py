from typing import Dict, Any, List
from langchain_core.tools import tool
import requests
from datetime import datetime, timedelta
import os
import feedparser
import time
import random

print("🛠️  Carregando ferramentas financeiras...")


ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

@tool
def get_stock_price(symbol: str) -> Dict[str, Any]:
    """Get current stock price and basic information for a given stock symbol."""
    print(f"📈 Buscando preço da ação: {symbol}")
    try:
        symbol = symbol.upper().strip()
        

        if ALPHA_VANTAGE_API_KEY:
            url = f"https://www.alphavantage.co/query"
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': ALPHA_VANTAGE_API_KEY
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'Global Quote' in data and data['Global Quote']:
                quote = data['Global Quote']
                return {
                    "symbol": symbol,
                    "current_price": float(quote.get('05. price', 0)),
                    "change": quote.get('09. change', 'N/A'),
                    "change_percent": quote.get('10. change percent', 'N/A'),
                    "high": quote.get('03. high', 'N/A'),
                    "low": quote.get('04. low', 'N/A'),
                    "volume": quote.get('06. volume', 'N/A'),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source": "Alpha Vantage"
                }
        

        print("⚠️  Usando dados mock para desenvolvimento")
        mock_prices = {
            "AAPL": 182.50, "MSFT": 415.86, "GOOGL": 175.25, 
            "TSLA": 245.18, "AMZN": 178.55, "META": 485.33,
            "NVDA": 925.88, "NFLX": 645.20
        }
        
        price = mock_prices.get(symbol, 100.00)
        return {
            "symbol": symbol,
            "current_price": price,
            "change": "+1.25",
            "change_percent": "+0.68%",
            "high": price + 2.5,
            "low": price - 2.5,
            "volume": "45,823,491",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "Mock Data (Yahoo Finance bloqueado)",
            "note": "Dados de exemplo para desenvolvimento"
        }
        
    except Exception as e:
        print(f"❌ Erro em get_stock_price para {symbol}: {e}")
        return {
            "symbol": symbol,
            "current_price": 150.00,  # Valor padrão
            "error": "Serviço temporariamente indisponível",
            "source": "Fallback",
            "note": "Use dados mock para continuar desenvolvimento"
        }

@tool
def get_stock_history(symbol: str, period: str = "1mo") -> Dict[str, Any]:
    """Get historical stock data for analysis."""
    print(f"📊 Buscando histórico: {symbol} período: {period}")
    try:
        symbol = symbol.upper().strip()
        
        
        print("⚠️  Usando dados históricos mock")
        
        
        base_price = 180.00
        if symbol == "AAPL": base_price = 182.50
        elif symbol == "MSFT": base_price = 415.86
        elif symbol == "TSLA": base_price = 245.18
        
        
        import random
        price_variation = random.uniform(-0.1, 0.1)  # ±10%
        current_price = base_price * (1 + price_variation)
        
        return {
            "symbol": symbol,
            "period": period,
            "performance": {
                "start_price": round(base_price * 0.95, 2),
                "end_price": round(current_price, 2),
                "price_change": round(current_price - base_price * 0.95, 2),
                "price_change_percent": round(((current_price - base_price * 0.95) / (base_price * 0.95)) * 100, 2),
                "highest_price": round(base_price * 1.05, 2),
                "lowest_price": round(base_price * 0.90, 2)
            },
            "source": "Mock Data",
            "note": "Dados históricos simulados para desenvolvimento"
        }
        
    except Exception as e:
        print(f"❌ Erro em get_stock_history para {symbol}: {e}")
        return {
            "error": f"Erro ao buscar histórico de {symbol}",
            "symbol": symbol,
            "period": period
        }

@tool
def calculate_portfolio_metrics(investments: List[Dict]) -> Dict[str, Any]:
    """Calculate portfolio performance metrics."""
    print(f"💼 Calculando portfólio com {len(investments)} investimentos")
    try:
        portfolio_details = []
        total_investment = 0
        current_value = 0
        
        for investment in investments:
            symbol = investment.get('symbol', '').upper().strip()
            shares = investment.get('shares', 0)
            purchase_price = investment.get('purchase_price', 0)
            
            if symbol and shares > 0:
                
                stock_data = get_stock_price.invoke({"symbol": symbol})
                current_price = stock_data.get('current_price', purchase_price)
                
                investment_amount = shares * purchase_price
                current_val = current_price * shares
                
                total_investment += investment_amount
                current_value += current_val
                
                profit_loss = current_val - investment_amount
                profit_loss_percent = (profit_loss / investment_amount) * 100 if investment_amount > 0 else 0
                
                portfolio_details.append({
                    "symbol": symbol,
                    "shares": shares,
                    "purchase_price": purchase_price,
                    "current_price": round(current_price, 2),
                    "investment_value": round(investment_amount, 2),
                    "current_value": round(current_val, 2),
                    "profit_loss": round(profit_loss, 2),
                    "profit_loss_percent": round(profit_loss_percent, 2)
                })
        
        total_return = current_value - total_investment
        return_percentage = (total_return / total_investment) * 100 if total_investment > 0 else 0
        
        return {
            "portfolio_details": portfolio_details,
            "summary": {
                "total_investment": round(total_investment, 2),
                "current_value": round(current_value, 2),
                "total_return": round(total_return, 2),
                "return_percentage": round(return_percentage, 2),
                "investments_count": len(portfolio_details)
            },
            "source": "Mock Data",
            "note": "Cálculos baseados em dados simulados"
        }
        
    except Exception as e:
        print(f"❌ Erro em calculate_portfolio_metrics: {e}")
        return {
            "error": "Erro ao calcular métricas do portfólio",
            "details": str(e)
        }

@tool
def get_market_news(symbol: str = None) -> Dict[str, Any]:
    """Get latest financial market news."""
    print(f"📰 Buscando notícias para: {symbol if symbol else 'mercado geral'}")
    try:
        if symbol:
            symbol = symbol.upper().strip()
            rss_url = f"https://news.google.com/rss/search?q={symbol}+stock+OR+{symbol}+investing&hl=en-US&gl=US&ceid=US:en"
        else:
            rss_url = "https://news.google.com/rss/search?q=stock+market+OR+investing+OR+finance&hl=en-US&gl=US&ceid=US:en"
        
        feed = feedparser.parse(rss_url)
        
        articles = []
        for entry in feed.entries[:6]:
            articles.append({
                "title": entry.title,
                "description": getattr(entry, 'description', 'No description available'),
                "url": entry.link,
                "publishedAt": getattr(entry, 'published', ''),
                "source": "Google News"
            })
        
        return {
            "source": "Google News RSS",
            "symbol": symbol,
            "articles_count": len(articles),
            "articles": articles
        }
        
    except Exception as e:
        print(f"❌ Erro em get_market_news: {e}")
        return {
            "error": "Erro ao buscar notícias",
            "details": str(e)
        }

@tool
def financial_calculator(operation: str, values: Dict[str, float]) -> Dict[str, Any]:
    """Perform financial calculations with precise formulas.
    Operations: compound_interest, loan_payment, roi
    For compound_interest: provide principal, rate, years, compounding_frequency (optional, default=1)"""
    print(f"🧮 Calculando: {operation} com valores: {values}")
    try:
        if operation == "compound_interest":
            principal = values.get('principal', 0)
            annual_rate = values.get('rate', 0) / 100  
            years = values.get('years', 0)
            compounding_frequency = values.get('compounding_frequency', 1)  
            
           
            future_value = principal * (1 + annual_rate/compounding_frequency) ** (compounding_frequency * years)
            interest_earned = future_value - principal
            
           
            calculation_steps = {
                "principal": principal,
                "annual_rate_decimal": annual_rate,
                "years": years,
                "compounding_frequency": compounding_frequency,
                "periodic_rate": annual_rate / compounding_frequency,
                "total_periods": compounding_frequency * years,
                "growth_factor": (1 + annual_rate/compounding_frequency) ** (compounding_frequency * years)
            }
            
            return {
                "operation": "compound_interest",
                "inputs": {
                    "principal": principal,
                    "annual_rate_percent": values.get('rate', 0),
                    "years": years,
                    "compounding_frequency": compounding_frequency
                },
                "results": {
                    "future_value": round(future_value, 2),
                    "interest_earned": round(interest_earned, 2),
                    "total_return_percent": round((interest_earned / principal) * 100, 2) if principal > 0 else 0
                },
                "formula": "A = P (1 + r/n)^(nt)",
                "calculation_steps": calculation_steps,
                "explanation": f"${principal:,.2f} at {values.get('rate', 0)}% annual interest compounded {compounding_frequency}x per year for {years} years"
            }
        
        elif operation == "loan_payment":
            principal = values.get('principal', 0)
            annual_rate = values.get('rate', 0) / 100
            monthly_rate = annual_rate / 12
            months = values.get('months', 0)
            
            if monthly_rate == 0:  
                monthly_payment = principal / months
            else:
                monthly_payment = (principal * monthly_rate) / (1 - (1 + monthly_rate) ** -months)
            
            total_payment = monthly_payment * months
            total_interest = total_payment - principal
            
            return {
                "operation": "loan_payment",
                "inputs": {
                    "principal": principal,
                    "annual_rate_percent": values.get('rate', 0),
                    "loan_term_months": months
                },
                "results": {
                    "monthly_payment": round(monthly_payment, 2),
                    "total_payment": round(total_payment, 2),
                    "total_interest": round(total_interest, 2),
                    "interest_to_principal_ratio": round((total_interest / principal) * 100, 2) if principal > 0 else 0
                },
                "formula": "PMT = P * (r(1+r)^n) / ((1+r)^n - 1)"
            }
        
        elif operation == "roi":
            investment = values.get('investment', 0)
            returns = values.get('returns', 0)
            net_profit = returns - investment
            roi_percentage = (net_profit / investment) * 100 if investment > 0 else 0
            
            return {
                "operation": "roi",
                "inputs": {
                    "investment": investment,
                    "returns": returns
                },
                "results": {
                    "net_profit": round(net_profit, 2),
                    "roi_percentage": round(roi_percentage, 2),
                    "multiple": round(returns / investment, 2) if investment > 0 else 0
                },
                "formula": "ROI = (Returns - Investment) / Investment * 100%"
            }
        
        elif operation == "future_value_simple":
            
            principal = values.get('principal', 0)
            rate = values.get('rate', 0) / 100
            years = values.get('years', 0)
            
            future_value = principal * (1 + rate) ** years
            interest_earned = future_value - principal
            
            return {
                "operation": "future_value_simple",
                "inputs": {
                    "principal": principal,
                    "rate_percent": values.get('rate', 0),
                    "years": years
                },
                "results": {
                    "future_value": round(future_value, 2),
                    "interest_earned": round(interest_earned, 2)
                },
                "formula": "FV = P (1 + r)^t",
                "note": "Assumes annual compounding"
            }
            
        else:
            return {
                "error": f"Operação desconhecida: {operation}",
                "available_operations": [
                    "compound_interest", 
                    "loan_payment", 
                    "roi",
                    "future_value_simple"
                ],
                "example_usage": {
                    "compound_interest": {"principal": 10000, "rate": 7, "years": 10},
                    "loan_payment": {"principal": 20000, "rate": 5, "months": 36},
                    "roi": {"investment": 5000, "returns": 7500}
                }
            }
            
    except Exception as e:
        print(f"❌ Erro em financial_calculator: {e}")
        return {
            "error": f"Erro no cálculo: {str(e)}",
            "operation": operation,
            "values": values
        }