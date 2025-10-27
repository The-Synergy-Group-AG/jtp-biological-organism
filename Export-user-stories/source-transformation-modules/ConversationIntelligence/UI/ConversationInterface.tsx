/**
 * AI-First Conversation Interface Component
 * 
 * Pure conversational UI - NO FORMS, NO BUTTONS, just natural chat
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { conversationEngine } from '../ConversationEngine';
import { AIResponse } from '../Types/ConversationTypes';

interface Message {
  id: string;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
  emotion?: string;
  isTyping?: boolean;
}

export const ConversationInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      type: 'ai',
      content: "Hi! I'm here to help you discover your ideal career path. What brings you here today?",
      timestamp: new Date(),
      emotion: 'supportive'
    }
  ]);
  const [input, setInput] = useState('');
  const [isAiTyping, setIsAiTyping] = useState(false);
  const [userId] = useState(`user_${Date.now()}`);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check-in after inactivity
  useEffect(() => {
    const checkInTimer = setTimeout(async () => {
      const checkIn = await conversationEngine.checkIn(userId);
      if (checkIn) {
        addMessage('ai', checkIn.message, checkIn.emotion);
      }
    }, 180000); // 3 minutes

    return () => clearTimeout(checkInTimer);
  }, [messages, userId]);

  const addMessage = (type: 'user' | 'ai', content: string, emotion?: string) => {
    const message: Message = {
      id: `msg_${Date.now()}_${Math.random()}`,
      type,
      content,
      timestamp: new Date(),
      emotion
    };
    setMessages(prev => [...prev, message]);
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input.trim();
    setInput('');
    
    // Add user message
    addMessage('user', userMessage);
    
    // Show AI typing
    setIsAiTyping(true);
    
    try {
      // Get AI response
      const response: AIResponse = await conversationEngine.chat(userId, userMessage);
      
      // Simulate typing delay for natural feel
      const typingDelay = Math.min(response.message.length * 10, 2000);
      
      setTimeout(() => {
        setIsAiTyping(false);
        addMessage('ai', response.message, response.emotion);
        
        // Handle suggested actions
        if (response.suggestedAction) {
          setTimeout(() => {
            addMessage('ai', response.suggestedAction, 'encouraging');
          }, 1000);
        }
      }, typingDelay);
      
    } catch (error) {
      setIsAiTyping(false);
      addMessage('ai', "I'm having trouble understanding that. Could you rephrase it?", 'supportive');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const getEmotionColor = (emotion?: string): string => {
    const emotionColors: Record<string, string> = {
      supportive: '#10B981',
      encouraging: '#3B82F6',
      celebratory: '#F59E0B',
      empathetic: '#8B5CF6',
      motivating: '#EF4444',
      calming: '#6EE7B7',
      energizing: '#FBBF24',
      reflective: '#6366F1'
    };
    return emotionColors[emotion || 'supportive'] || '#10B981';
  };

  const renderMessage = (message: Message) => {
    const isUser = message.type === 'user';
    
    return (
      <div
        key={message.id}
        className={`mb-4 ${isUser ? 'text-right' : 'text-left'}`}
      >
        <div
          className={`inline-block max-w-[80%] px-4 py-3 rounded-2xl ${
            isUser
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 text-gray-800'
          }`}
          style={{
            borderBottomColor: !isUser ? getEmotionColor(message.emotion) : undefined,
            borderBottomWidth: !isUser ? '3px' : undefined,
            borderBottomStyle: !isUser ? 'solid' : undefined
          }}
        >
          <p className="whitespace-pre-wrap">{message.content}</p>
          <p className={`text-xs mt-1 ${isUser ? 'text-blue-100' : 'text-gray-500'}`}>
            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </p>
        </div>
      </div>
    );
  };

  return (
    <div className="flex flex-col h-screen bg-white">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 shadow-lg">
        <h1 className="text-2xl font-bold">Career Discovery Conversation</h1>
        <p className="text-sm opacity-90">Let's explore your career journey together</p>
      </div>

      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {messages.map(renderMessage)}
        
        {isAiTyping && (
          <div className="text-left mb-4">
            <div className="inline-block bg-gray-100 text-gray-800 px-4 py-3 rounded-2xl">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="border-t bg-white p-4">
        <div className="flex space-x-2">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Share your thoughts... (Press Enter to send)"
            className="flex-1 px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleSend}
            className="px-6 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-colors"
          >
            Send
          </button>
        </div>
        
        {/* Quick insights */}
        <div className="mt-3 flex space-x-2 text-sm">
          <button
            onClick={async () => {
              const insights = await conversationEngine.getInsights(userId);
              const summary = await conversationEngine.generateJourneySummary(userId);
              addMessage('ai', summary, 'reflective');
            }}
            className="text-blue-600 hover:underline"
          >
            View Journey Summary
          </button>
          <span className="text-gray-400">•</span>
          <button
            onClick={() => {
              addMessage('user', "I'm feeling stuck and don't know what to do");
              handleSend();
            }}
            className="text-purple-600 hover:underline"
          >
            Need Support
          </button>
        </div>
      </div>
    </div>
  );
};