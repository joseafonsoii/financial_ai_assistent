import React, { useState, useRef, useEffect } from 'react';
import { Send, Brain, TrendingUp, Calculator } from 'lucide-react';
import { chatWithAI } from '../services/api';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { type: 'user', content: input, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await chatWithAI(input, messages);
      
      const aiMessage = {
        type: 'ai',
        content: response.response,
        tool_calls: response.tool_calls || [],
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error(error);
      const errorMessage = {
        type: 'error',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const quickActions = [
    {
      title: "Stock Analysis",
      prompt: "What is the current price of Apple stock (AAPL) and show me its performance over the last month?",
      icon: TrendingUp
    },
    {
      title: "Portfolio Check",
      prompt: "Calculate my portfolio performance: 10 shares of AAPL at $150 each and 5 shares of MSFT at $300 each",
      icon: Brain
    },
    {
      title: "Financial Calc",
      prompt: "Calculate compound interest for $10,000 at 7% annual return over 10 years",
      icon: Calculator
    }
  ];

  const handleQuickAction = (prompt) => {
    setInput(prompt);
  };

  // Estilos inline para substituir o Tailwind
  const styles = {
    container: {
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #eff6ff 0%, #e0e7ff 100%)',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    },
    header: {
      textAlign: 'center',
      marginBottom: '2rem'
    },
    headerContent: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '12px',
      marginBottom: '1rem'
    },
    iconWrapper: {
      padding: '12px',
      backgroundColor: '#2563eb',
      borderRadius: '50%'
    },
    title: {
      fontSize: '2.25rem',
      fontWeight: 'bold',
      color: '#1f2937',
      margin: 0
    },
    subtitle: {
      color: '#6b7280',
      fontSize: '1.125rem',
      margin: 0
    },
    quickActions: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
      gap: '1rem',
      marginBottom: '1.5rem'
    },
    quickActionButton: {
      padding: '1rem',
      backgroundColor: 'white',
      borderRadius: '0.5rem',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
      border: '1px solid #e5e7eb',
      textAlign: 'left',
      cursor: 'pointer',
      transition: 'box-shadow 0.2s ease',
      outline: 'none'
    },
    quickActionButtonHover: {
      boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
    },
    chatContainer: {
      backgroundColor: 'white',
      borderRadius: '1rem',
      boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
      overflow: 'hidden'
    },
    messages: {
      height: '24rem',
      overflowY: 'auto',
      padding: '1.5rem'
    },
    messageRow: {
      display: 'flex',
      marginBottom: '1rem'
    },
    messageRowUser: {
      justifyContent: 'flex-end'
    },
    messageBubble: {
      maxWidth: '75%',
      borderRadius: '1rem',
      padding: '0.75rem 1rem'
    },
    userBubble: {
      backgroundColor: '#2563eb',
      color: 'white',
      borderBottomRightRadius: '0'
    },
    aiBubble: {
      backgroundColor: '#f3f4f6',
      color: '#1f2937',
      borderBottomLeftRadius: '0'
    },
    errorBubble: {
      backgroundColor: '#fef2f2',
      color: '#991b1b',
      border: '1px solid #fecaca',
      borderBottomLeftRadius: '0'
    },
    inputArea: {
      borderTop: '1px solid #e5e7eb',
      padding: '1rem'
    },
    inputContainer: {
      display: 'flex',
      gap: '1rem'
    },
    textarea: {
      flex: 1,
      border: '1px solid #d1d5db',
      borderRadius: '1rem',
      padding: '0.75rem 1rem',
      fontSize: '1rem',
      resize: 'none',
      outline: 'none',
      fontFamily: 'inherit'
    },
    textareaFocus: {
      borderColor: '#3b82f6',
      boxShadow: '0 0 0 2px rgba(59, 130, 246, 0.2)'
    },
    sendButton: {
      backgroundColor: '#2563eb',
      color: 'white',
      borderRadius: '1rem',
      padding: '0.75rem 1.5rem',
      border: 'none',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      outline: 'none'
    },
    sendButtonHover: {
      backgroundColor: '#1d4ed8'
    },
    sendButtonDisabled: {
      opacity: 0.5,
      cursor: 'not-allowed'
    },
    loadingDots: {
      display: 'flex',
      gap: '0.25rem'
    },
    dot: {
      width: '0.5rem',
      height: '0.5rem',
      backgroundColor: '#9ca3af',
      borderRadius: '50%',
      animation: 'bounce 1.4s infinite ease-in-out'
    },
    emptyState: {
      textAlign: 'center',
      color: '#6b7280',
      marginTop: '4rem'
    }
  };

  return (
    <div style={styles.container}>
      <div style={{ maxWidth: '56rem', margin: '0 auto', padding: '2rem 1rem' }}>
        {/* Header */}
        <div style={styles.header}>
          <div style={styles.headerContent}>
            <div style={styles.iconWrapper}>
              <Brain size={32} color="white" />
            </div>
            <h1 style={styles.title}>Financial AI Assistant</h1>
          </div>
          <p style={styles.subtitle}>
            Advanced AI-powered financial analysis and portfolio management
          </p>
        </div>

        {/* Quick Actions */}
        <div style={styles.quickActions}>
          {quickActions.map((action, index) => {
            const IconComponent = action.icon;
            return (
              <button
                key={index}
                onClick={() => handleQuickAction(action.prompt)}
                style={styles.quickActionButton}
                onMouseOver={(e) => {
                  e.target.style.boxShadow = styles.quickActionButtonHover.boxShadow;
                }}
                onMouseOut={(e) => {
                  e.target.style.boxShadow = styles.quickActionButton.boxShadow;
                }}
              >
                <IconComponent size={24} color="#2563eb" style={{ marginBottom: '0.5rem' }} />
                <h3 style={{ fontWeight: 600, color: '#1f2937', margin: '0 0 0.25rem 0' }}>
                  {action.title}
                </h3>
                <p style={{ fontSize: '0.875rem', color: '#6b7280', margin: 0, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {action.prompt}
                </p>
              </button>
            );
          })}
        </div>

        {/* Chat Container */}
        <div style={styles.chatContainer}>
          {/* Messages */}
          <div style={styles.messages}>
            {messages.length === 0 ? (
              <div style={styles.emptyState}>
                <Brain size={64} color="#d1d5db" style={{ margin: '0 auto 1rem auto' }} />
                <p style={{ fontSize: '1.125rem', margin: 0 }}>
                  Ask me about stocks, portfolios, or financial calculations!
                </p>
              </div>
            ) : (
              messages.map((message, index) => (
                <div
                  key={index}
                  style={{
                    ...styles.messageRow,
                    ...(message.type === 'user' ? styles.messageRowUser : {})
                  }}
                >
                  <div
                    style={{
                      ...styles.messageBubble,
                      ...(message.type === 'user' 
                        ? styles.userBubble 
                        : message.type === 'error'
                        ? styles.errorBubble
                        : styles.aiBubble)
                    }}
                  >
                    <div style={{ whiteSpace: 'pre-wrap' }}>{message.content}</div>
                    {message.tool_calls && message.tool_calls.length > 0 && (
                      <div style={{ marginTop: '0.5rem', fontSize: '0.75rem', opacity: 0.75 }}>
                        Used tools: {message.tool_calls.map(tc => tc.name).join(', ')}
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
            {loading && (
              <div style={styles.messageRow}>
                <div style={{ ...styles.messageBubble, ...styles.aiBubble }}>
                  <div style={styles.loadingDots}>
                    <div style={{ ...styles.dot, animationDelay: '0s' }}></div>
                    <div style={{ ...styles.dot, animationDelay: '0.2s' }}></div>
                    <div style={{ ...styles.dot, animationDelay: '0.4s' }}></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div style={styles.inputArea}>
            <div style={styles.inputContainer}>
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about stocks, portfolios, financial calculations..."
                style={styles.textarea}
                rows="2"
                disabled={loading}
                onFocus={(e) => {
                  e.target.style.borderColor = styles.textareaFocus.borderColor;
                  e.target.style.boxShadow = styles.textareaFocus.boxShadow;
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = styles.textarea.borderColor;
                  e.target.style.boxShadow = 'none';
                }}
              />
              <button
                onClick={handleSend}
                disabled={loading || !input.trim()}
                style={{
                  ...styles.sendButton,
                  ...(loading || !input.trim() ? styles.sendButtonDisabled : {})
                }}
                onMouseOver={(e) => {
                  if (!loading && input.trim()) {
                    e.target.style.backgroundColor = styles.sendButtonHover.backgroundColor;
                  }
                }}
                onMouseOut={(e) => {
                  if (!loading && input.trim()) {
                    e.target.style.backgroundColor = styles.sendButton.backgroundColor;
                  }
                }}
              >
                <Send size={20} />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Adicionar animação CSS para os dots */}
      <style>
        {`
          @keyframes bounce {
            0%, 80%, 100% {
              transform: scale(0);
            }
            40% {
              transform: scale(1);
            }
          }
        `}
      </style>
    </div>
  );
};

export default ChatInterface;