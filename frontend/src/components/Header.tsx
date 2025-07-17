import React from 'react';
import { Bot, Wifi, WifiOff } from 'lucide-react';

interface HeaderProps {
  isConnected?: boolean;
}

const Header: React.FC<HeaderProps> = ({ isConnected = true }) => {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <div className="logo">
            <Bot className="logo-icon" />
            <span className="logo-text">PulseAI</span>
          </div>
          <div className="tagline">Intelligent HR Assistant</div>
        </div>
        
        <div className="header-right">
          <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
            {isConnected ? (
              <>
                <Wifi className="status-icon" />
                <span>Connected</span>
              </>
            ) : (
              <>
                <WifiOff className="status-icon" />
                <span>Disconnected</span>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header; 
