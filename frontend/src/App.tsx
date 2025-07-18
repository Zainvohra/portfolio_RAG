import React, { useState } from 'react';
import './App.css';
import ChatInterface from './components/ChatInterface';
import Header from './components/Header';

export interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  isLoading?: boolean;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'Hello! I\'m PulseAI, your intelligent assistant. How can I help you today?',
      sender: 'ai',
      timestamp: new Date()
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: text.trim(),
      sender: 'user',
      timestamp: new Date()
    };

    const aiMessage: Message = {
      id: (Date.now() + 1).toString(),
      text: '',
      sender: 'ai',
      timestamp: new Date(),
      isLoading: true
    };

    setMessages(prev => [...prev, userMessage, aiMessage]);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/pulse/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: text })
      }); 
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const agentResponse = await response.text();
      
      setMessages(prev => prev.map(msg => 
        msg.id === aiMessage.id 
          ? { ...msg, text: agentResponse, isLoading: false }
          : msg
      ));
    } catch (error) {
      setMessages(prev => prev.map(msg => 
        msg.id === aiMessage.id 
          ? { ...msg, text: 'Sorry, I encountered an error. Please try again.', isLoading: false }
          : msg
      ));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <Header />
      <ChatInterface 
        messages={messages}
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
      />
    </div>
  );
}

export default App;
