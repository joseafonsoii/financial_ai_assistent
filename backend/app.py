from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

print("🔧 Iniciando servidor Flask com Gemini...")

load_dotenv()


api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ ERRO: GEMINI_API_KEY não encontrada no arquivo .env")
    print("💡 Crie/atualize o arquivo .env com: GEMINI_API_KEY=sua_chave_gemini_aqui")
    print("🔑 Obtenha em: https://aistudio.google.com/app/apikey")
    exit(1)
else:
    print(f"✅ GEMINI_API_KEY carregada: {api_key[:10]}...")

app = Flask(__name__)
CORS(app)

print("🔄 Carregando agente financeiro com Gemini...")
try:
    from agents.financial_agent import financial_agent
    print("✅ Agente financeiro com Gemini carregado com sucesso!")
except Exception as e:
    print(f"❌ Erro carregando agente: {e}")
    exit(1)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy", 
        "service": "Financial AI Assistant with Gemini",
        "model": "Gemini 1.5 Flash"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        print(f"💬 Mensagem recebida: {user_message}")
        
    
        messages = [HumanMessage(content=user_message)]
        inputs = {"messages": messages}
        

        print("🔄 Processando com Gemini...")
        response = financial_agent.invoke(inputs)
        last_message = response["messages"][-1]
        
        
        result = {
            "response": last_message.content,
            "success": True,
            "model": "Gemini 1.5 Flash"
        }
        

        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            result["tools_used"] = [tool_call['name'] for tool_call in last_message.tool_calls]
        
        print("✅ Resposta gerada com sucesso pelo Gemini")
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Erro no chat: {e}")
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

@app.route('/')
def home():
    """Home page"""
    return jsonify({
        "message": "Financial AI Assistant API with Google Gemini",
        "model": "Gemini 1.5 Flash",
        "endpoints": {
            "GET /api/health": "Health check",
            "POST /api/chat": "Chat with AI assistant"
        }
    })

if __name__ == '__main__':
    print("🚀 Servidor com Gemini iniciando na porta 5000...")
    print("📍 Endpoints disponíveis:")
    print("   http://localhost:5000/api/health")
    print("   http://localhost:5000/api/chat")
    print("   http://localhost:5000/")
    print("💡 Teste com: 'What is Apple stock price?'")
    app.run(debug=True, port=5000)