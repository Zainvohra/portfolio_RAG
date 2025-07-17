import React, { useState, useRef, useEffect } from 'react';
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
      // TODO: Replace with actual API call to your FastAPI backend
      // const response = await fetch('/api/chat', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ message: text })
      // });
      // const data = await response.json();

      // Simulate API response for now
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const mockResponse = getMockResponse(text);
      
      setMessages(prev => prev.map(msg => 
        msg.id === aiMessage.id 
          ? { ...msg, text: mockResponse, isLoading: false }
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

  const getMockResponse = (userInput: string): string => {
    const input = userInput.toLowerCase();
    
    if (input.includes('onboarding') || input.includes('email')) {
      return 'I\'ve sent all pending onboarding emails to new employees. The status has been updated in the database.';
    } else if (input.includes('attendance') || input.includes('missing')) {
      return 'I found 3 employees with missing attendance records in the last 30 days. Would you like me to send them reminders?';
    } else if (input.includes('report') || input.includes('july')) {
      return 'Here\'s your attendance report from July 15 to July 30:\n\n• July 15: In 9:00 AM, Out 5:30 PM\n• July 16: In 8:45 AM, Out 5:15 PM\n• July 17: Missing punch (in)\n• July 18: In 9:15 AM, Out 5:45 PM\n\nYou had 1 violation this period.';
    } else if (input.includes('meeting') || input.includes('notes')) {
      return 'I\'ve sent reminder emails to 5 employees who haven\'t submitted their LM meeting notes for this quarter yet.';
    } else {
      return 'I understand you\'re asking about "' + userInput + '". I can help you with:\n\n• Sending onboarding emails\n• Identifying missing attendance\n• Generating attendance reports\n• Sending meeting notes reminders\n\nWhat would you like me to do?';
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
