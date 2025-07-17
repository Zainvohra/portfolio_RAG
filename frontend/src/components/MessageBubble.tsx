import React from 'react';
import { User, Bot } from 'lucide-react';
import { Message } from '../App';

interface MessageBubbleProps {
  message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const formatText = (text: string) => {
    // Convert newlines to <br> tags and preserve formatting
    return text.split('\n').map((line, index) => (
      <React.Fragment key={index}>
        {line}
        {index < text.split('\n').length - 1 && <br />}
      </React.Fragment>
    ));
  };

  return (
    <div className={`message ${message.sender}-message`}>
      <div className="message-avatar">
        {message.sender === 'user' ? (
          <User className="avatar-icon user-avatar" />
        ) : (
          <Bot className="avatar-icon ai-avatar" />
        )}
      </div>
      
      <div className="message-content">
        <div className="message-header">
          <span className="message-sender">
            {message.sender === 'user' ? 'You' : 'PulseAI'}
          </span>
          <span className="message-time">
            {formatTime(message.timestamp)}
          </span>
        </div>
        
        <div className="message-text">
          {message.isLoading ? (
            <div className="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          ) : (
            formatText(message.text)
          )}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble; 
