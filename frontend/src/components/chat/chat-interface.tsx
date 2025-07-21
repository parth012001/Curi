"use client"

import { useState, useRef, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Send, RefreshCw, ExternalLink } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ChatMessageComponent } from "./chat-message"
import { ChatMessage, apiCall, ChatResponse } from "@/lib/utils"
import { useSession } from "next-auth/react"

export function ChatInterface() {
  const { data: session } = useSession()
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [currentTopic, setCurrentTopic] = useState("")
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const userName = session?.user?.name || session?.user?.email?.split('@')[0] || 'John'

  const suggestedPrompts = [
    "Can you suggest the best long-lasting brown lipstick",
    "What's a good foundation for oily skin that doesn't look cakey?",
    "I need a gentle face cleanser for sensitive skin—any recommendations?",
    "What's a good everyday mascara that doesn't smudge?"
  ]

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (messageText?: string) => {
    const textToSend = messageText || input.trim()
    if (!textToSend || isLoading) return

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: textToSend,
      role: "user",
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    if (!messageText) setInput("")
    setIsLoading(true)

    try {
      const response: ChatResponse = await apiCall("/chat", {
        method: "POST",
        body: JSON.stringify({ message: textToSend, history: messages }),
      })

      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: response.response,
        role: "assistant",
        timestamp: new Date(),
        products: response.products,
        insights: response.insights,
        confidence: response.confidence,
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error("Error sending message:", error)
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: "Sorry, I encountered an error. Please try again.",
        role: "assistant",
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  // If there are messages, show the chat interface
  if (messages.length > 0) {
    return (
      <div className="flex flex-col h-[calc(100vh-80px)] w-full max-w-6xl mx-auto">
        {/* Topic Header */}
        {currentTopic && (
          <div className="px-6 py-4 border-b border-gray-200 bg-white">
            <h1 className="text-2xl font-bold text-gray-800" style={{ fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif' }}>
              {currentTopic}
            </h1>
          </div>
        )}

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-white">
          <AnimatePresence mode="wait">
            {messages.map((message, index) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -20, scale: 0.95 }}
                transition={{ 
                  duration: 0.3, 
                  delay: index * 0.1,
                  type: "spring",
                }}
                className={
                  message.role === 'user'
                    ? 'flex justify-end items-start gap-3'
                    : 'flex justify-start items-start gap-3'
                }
              >
                {message.role === 'assistant' && (
                  <div className="w-8 h-8 rounded-full bg-gray-800 flex items-center justify-center flex-shrink-0">
                    <span className="text-white font-bold text-sm">C</span>
                  </div>
                )}
                
                <div
                  className={
                    message.role === 'user'
                      ? 'bg-gray-100 text-gray-800 rounded-2xl px-5 py-3 max-w-[70%] shadow-lg'
                      : 'bg-gray-100 text-gray-800 rounded-2xl px-5 py-3 max-w-[80%] shadow-md'
                  }
                  style={{ fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif' }}
                >
                  <ChatMessageComponent message={message} />
                </div>

                {message.role === 'user' && (
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center flex-shrink-0">
                    <span className="text-white font-semibold text-sm">{userName.charAt(0).toUpperCase()}</span>
                  </div>
                )}
              </motion.div>
            ))}
          </AnimatePresence>
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="p-6 border-t border-gray-200 bg-white">
          <div className="flex items-center gap-3">
            <div className="flex-1">
              <textarea
                className="w-full p-3 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="Ask me about beauty products...."
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={handleKeyPress}
                disabled={isLoading}
                rows={1}
                style={{ fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif', minHeight: '36px' }}
              />
            </div>
            {/* Send Button */}
            <Button
              onClick={() => handleSendMessage()}
              disabled={isLoading || !input.trim()}
              className="bg-green-500 hover:bg-green-600 text-white rounded-lg shadow-md transition-colors border-none h-12 w-12 flex items-center justify-center p-0 mt-1"
            >
              <Send className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </div>
    )
  }

  // Initial welcome screen
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-80px)] w-full max-w-4xl mx-auto px-6">
      {/* Greeting */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2" style={{ fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif' }}>
          Hi there, {userName}
        </h1>
        <h2 className="text-3xl font-bold text-gray-800 mb-4" style={{ fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif' }}>
          What would you like to shop?
        </h2>
        <p className="text-gray-600 text-lg" style={{ fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif' }}>
          Use one of the most common prompts below or use your own to begin
        </p>
      </div>

      {/* Suggested Prompts */}
      <div className="grid grid-cols-2 gap-4 mb-12 w-full max-w-2xl">
        {suggestedPrompts.map((prompt, index) => (
          <motion.button
            key={index}
            onClick={() => handleSendMessage(prompt)}
            className="relative p-4 bg-gray-100 rounded-lg text-left hover:bg-gray-200 transition-colors group"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <ExternalLink className="absolute top-3 right-3 w-4 h-4 text-gray-400 group-hover:text-gray-600" />
            <p className="text-gray-800 font-medium pr-8" style={{ fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif' }}>
              {prompt}
            </p>
          </motion.button>
        ))}
      </div>

      {/* Input Area */}
      <div className="w-full max-w-2xl">
        <div className="flex items-start gap-3">
          <div className="flex-1">
            <textarea
              className="w-full p-3 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
              placeholder="Ask me about beauty products...."
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              disabled={isLoading}
              rows={1}
              style={{ fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif', minHeight: '36px' }}
            />
          </div>
          {/* Send Button */}
          <Button
            onClick={() => handleSendMessage()}
            disabled={isLoading || !input.trim()}
            className="bg-green-500 hover:bg-green-600 text-white rounded-lg shadow-md transition-colors border-none h-12 w-12 flex items-center justify-center p-0 mt-1"
          >
            <Send className="w-6 h-6" />
          </Button>
        </div>
      </div>
    </div>
  )
} 