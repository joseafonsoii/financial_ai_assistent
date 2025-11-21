from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import os

print("🤖 Iniciando Financial Agent com Google Gemini...")

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# Importar ferramentas
try:
    from agents.tools import (
        get_stock_price, 
        get_stock_history, 
        calculate_portfolio_metrics, 
        get_market_news, 
        financial_calculator
    )
    
    tools = [
        get_stock_price, 
        get_stock_history, 
        calculate_portfolio_metrics, 
        get_market_news, 
        financial_calculator
    ]
    
    print("✅ Todas as ferramentas importadas com sucesso!")
    
except ImportError as e:
    print(f"❌ Erro importando ferramentas: {e}")
    exit(1)

print(f"🎯 {len(tools)} ferramentas carregadas: {[t.name for t in tools]}")

# Configurar Google Gemini
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ GEMINI_API_KEY não encontrada no arquivo .env!")
    exit(1)
else:
    print(f"✅ Gemini API Key encontrada: {api_key[:10]}...")


available_models = [
    "gemini-2.0-flash",      
    "gemini-2.0-flash-001",    
    "gemini-2.0-flash-lite",   
    "gemini-pro-latest",      
    "gemini-2.5-flash",        
]

model_with_tools = None

for model_name in available_models:
    try:
        print(f"🔄 Tentando modelo: {model_name}")
        
        model = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=0,
            max_tokens=2048
        )
        
        # Teste simples
        test_response = model.invoke("Hello")
        print(f"✅ {model_name} funcionando!")
        
        # Bind tools
        model_with_tools = model.bind_tools(tools)
        print(f"✅ Ferramentas vinculadas ao {model_name}")
        break
        
    except Exception as e:
        print(f"❌ {model_name} falhou: {str(e)[:100]}...")
        continue

if model_with_tools is None:
    print("💥 Nenhum modelo funcionou!")
    print("💡 Tentando modelo fallback...")
    try:
        
        model = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=api_key,
            temperature=0
        )
        model_with_tools = model.bind_tools(tools)
        print("✅ Modelo fallback configurado!")
    except:
        print("💥 Todos os modelos falharam!")
        exit(1)

print("🚀 Modelo Gemini configurado com sucesso!")

def model_call(state: AgentState) -> AgentState:
    """Process messages with the AI model"""
    system_prompt = SystemMessage(content="""
    You are a sophisticated Financial AI Assistant. Your capabilities include:

        🔧 AVAILABLE TOOLS:
        - get_stock_price: Get current stock prices and info
        - get_stock_history: Get historical stock performance  
        - calculate_portfolio_metrics: Analyze investment portfolios
        - get_market_news: Get latest financial news
        - financial_calculator: Perform financial calculations

        📊 FOR FINANCIAL CALCULATIONS:
        ALWAYS use the financial_calculator tool for any math operations.
        For compound interest calculations, use operation: "compound_interest" with:
        - principal: initial amount
        - rate: annual interest rate (as percentage)
        - years: time period
        - compounding_frequency: optional (default=1 for annual)

        Example: For "$10,000 at 7% for 10 years" use:
        financial_calculator({
        "operation": "compound_interest", 
       "values": {"principal": 10000, "rate": 7, "years": 10}
        })

        NEVER try to calculate manually - always use the tool for accuracy.
    """)
    
    print("🔄 Processando pergunta com Gemini...")
    response = model_with_tools.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState):
    """Determine if we should continue to tools or end"""
    messages = state["messages"]
    last_message = messages[-1]
    
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        tool_names = [tool_call['name'] for tool_call in last_message.tool_calls]
        print(f"🛠️  Gemini decidiu usar ferramentas: {tool_names}")
        return "continue"
    else:
        print("💬 Gemini decidiu responder diretamente")
        return "end"


graph = StateGraph(AgentState)
graph.add_node("agent", model_call)
graph.add_node("tools", ToolNode(tools))
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"continue": "tools", "end": END})
graph.add_edge("tools", "agent")

financial_agent = graph.compile()
print("🚀 Financial Agent com Gemini pronto para uso!")