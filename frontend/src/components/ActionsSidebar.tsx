import React, { useState } from "react";
import { Copy, Check } from "lucide-react";
import { ACTIONS_LIST } from "../constants/actions";

const ActionsSidebar: React.FC<{ setInputText: (text: string) => void }> = ({
  setInputText,
}) => {
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>("All");

  const categories = [
    "All",
    ...Array.from(new Set(ACTIONS_LIST.map((action) => action.category))),
  ];
  const filteredActions =
    selectedCategory === "All"
      ? ACTIONS_LIST
      : ACTIONS_LIST.filter((action) => action.category === selectedCategory);

  const copyToClipboard = async (prompt: string, actionId: string) => {
    try {
      await navigator.clipboard.writeText(prompt);
      setCopiedId(actionId);
      const inputElement = document.getElementById("chat-input");
      if (inputElement) {
        setInputText(prompt);
      }
      setTimeout(() => setCopiedId(null), 2000);
    } catch (err) {
      console.error("Failed to copy text: ", err);
    }
  };

  return (
    <div className="sidebar">
      <div className="header">
        <h2 className="title">Quick Actions</h2>
        <p className="subtitle">
          Here is the list of actions you can perform with PulseAI 🤖
        </p>

        {/* Category Filter */}
        <div className="category-filters">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`category-button ${
                selectedCategory === category ? "active" : ""
              }`}
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      <div className="actions-container">
        {filteredActions.map((action) => (
          <div
            key={action.id}
            className="action-card"
            onClick={() => copyToClipboard(action.prompt, action.id)}
          >
            <div className="action-header">
              <div className="action-title-row">
                <div className="action-icon">{action.icon}</div>
                <h3 className="action-title">{action.title}</h3>
              </div>
              <div
                className={`copy-icon ${
                  copiedId === action.id ? "copied" : ""
                }`}
              >
                {copiedId === action.id ? <Check /> : <Copy />}
              </div>
            </div>

            <p className="action-description">{action.description}</p>

            <div className="prompt-container">
              <code className="prompt-code">{action.prompt}</code>
            </div>

            <div>
              <span className="category-tag">{action.category}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="footer">
        <div className="footer-content">
          <Copy className="footer-icon" />
          <span>Click any action above to copy the prompt</span>
        </div>
      </div>
    </div>
  );
};

export default ActionsSidebar;
