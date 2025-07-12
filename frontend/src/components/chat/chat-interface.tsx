"use client"

import { useState, useRef, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Send, Sparkles, Loader2, User, LogOut } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ChatMessageComponent } from "./chat-message"
import { ChatMessage, apiCall, ChatResponse } from "@/lib/utils"
import { useSession, signOut } from "next-auth/react"

export function ChatInterface() {
  const { data: session } = useSession()
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [showUserMenu, setShowUserMenu] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: input.trim(),
      role: "user",
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    try {
      const response: ChatResponse = await apiCall("/chat", {
        method: "POST",
        body: JSON.stringify({ message: input.trim() }),
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

  // Close user menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (showUserMenu) {
        setShowUserMenu(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [showUserMenu])

  return (
    <div className="flex flex-col h-[80vh] bg-white/70">
      {/* Header */}
      <div className="sticky top-0 z-10 flex items-center justify-between p-4 border-b border-gray-100 bg-white/80 backdrop-blur-md shadow-sm">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-r from-pink-500 to-purple-600 flex items-center justify-center shadow-md">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-lg text-gray-900 tracking-tight">Curi</h1>
            <p className="text-xs text-gray-500">Your beauty product assistant</p>
          </div>
        </div>
        
        {/* User Menu */}
        {session && (
          <div className="relative">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center gap-2"
            >
              <div className="w-8 h-8 rounded-full bg-gradient-to-r from-pink-500 to-purple-600 flex items-center justify-center">
                <User className="w-4 h-4 text-white" />
              </div>
              <span className="text-sm font-medium text-gray-700">
                {session.user?.name || session.user?.email?.split('@')[0] || 'User'}
              </span>
            </Button>
            
            {showUserMenu && (
              <div className="absolute right-0 top-full mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-100 py-2 z-50">
                <div className="px-4 py-2 border-b border-gray-100">
                  <p className="text-sm font-medium text-gray-900">
                    {session.user?.name || 'User'}
                  </p>
                  <p className="text-xs text-gray-500">
                    {session.user?.email}
                  </p>
                </div>
                <button
                  onClick={() => signOut({ callbackUrl: '/' })}
                  className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2"
                >
                  <LogOut className="w-4 h-4" />
                  Sign Out
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gradient-to-b from-white/60 to-purple-50/40">
        <AnimatePresence>
          {messages.map((message) => (
            <ChatMessageComponent key={message.id} message={message} />
          ))}
        </AnimatePresence>
        {/* Loading indicator */}
        {isLoading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex gap-3 p-4"
          >
            <div className="flex-shrink-0">
              <div className="w-8 h-8 rounded-full bg-gradient-to-r from-pink-500 to-purple-600 flex items-center justify-center">
                <Loader2 className="w-4 h-4 text-white animate-spin" />
              </div>
            </div>
            <div className="flex-1 max-w-3xl">
              <div className="inline-block p-4 rounded-2xl bg-white border border-gray-100 shadow-sm">
                <div className="flex items-center gap-2">
                  <Loader2 className="w-4 h-4 animate-spin text-gray-400" />
                  <span className="text-sm text-gray-500">Thinking...</span>
                </div>
              </div>
            </div>
          </motion.div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-100 bg-white/80 backdrop-blur-md">
        <div className="flex gap-2 shadow-lg rounded-xl bg-white px-3 py-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me about beauty products..."
            className="flex-1 bg-transparent border-none focus:ring-0 text-base"
            disabled={isLoading}
          />
          <Button
            onClick={handleSendMessage}
            disabled={!input.trim() || isLoading}
            variant="gradient"
            size="icon"
            className="shadow-md"
          >
            <Send className="w-4 h-4" />
          </Button>
        </div>
        {/* Quick suggestions */}
        {messages.length === 0 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4"
          >
            <p className="text-xs text-gray-400 mb-2">Try asking:</p>
            <div className="flex flex-wrap gap-2">
              {[
                "Find me a good moisturizer for dry skin",
                "What are the best lipsticks under $20?",
                "Recommend anti-aging products for sensitive skin",
                "Show me popular foundations"
              ].map((suggestion, index) => (
                <button
                  key={index}
                  onClick={() => setInput(suggestion)}
                  className="text-xs px-3 py-1 rounded-full bg-gradient-to-r from-pink-100 to-purple-100 hover:from-pink-200 hover:to-purple-200 text-pink-700 font-medium shadow-sm border border-pink-200 transition-colors"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
} 