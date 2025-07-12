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
  const [isSigningOut, setIsSigningOut] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Debug session
  useEffect(() => {
    console.log('Session:', session)
  }, [session])

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
      const target = event.target as Element
      const userMenu = target.closest('.user-menu')
      
      if (showUserMenu && !userMenu) {
        setShowUserMenu(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [showUserMenu])

  return (
    <div className="flex flex-col h-[80vh] bg-gradient-to-br from-white via-pink-50/30 to-purple-50/30 rounded-3xl shadow-2xl border border-white/20 overflow-hidden">
      {/* Header */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="sticky top-0 z-10 flex items-center justify-between p-6 border-b border-white/20 bg-white/90 backdrop-blur-xl shadow-lg"
      >
        <div className="flex items-center gap-4">
          <motion.div 
            whileHover={{ scale: 1.1, rotate: 5 }}
            className="w-12 h-12 rounded-2xl bg-gradient-to-r from-pink-500 via-purple-500 to-pink-600 flex items-center justify-center shadow-lg"
          >
            <Sparkles className="w-6 h-6 text-white" />
          </motion.div>
          <div>
            <h1 className="font-bold text-xl text-gray-900 tracking-tight">Curi</h1>
            <p className="text-sm text-gray-600">Your AI beauty assistant</p>
          </div>
        </div>
        
        {/* User Menu */}
        {session && (
          <motion.div 
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="relative user-menu"
          >
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center gap-3 px-4 py-2 rounded-xl bg-white/80 hover:bg-white shadow-md border border-white/20 transition-all duration-200"
            >
              <div className="w-8 h-8 rounded-full bg-gradient-to-r from-pink-500 to-purple-600 flex items-center justify-center shadow-sm">
                <User className="w-4 h-4 text-white" />
              </div>
              <span className="text-sm font-medium text-gray-700">
                {session.user?.name || session.user?.email?.split('@')[0] || 'User'}
              </span>
            </motion.button>
            
            <AnimatePresence>
              {showUserMenu && (
                <motion.div 
                  initial={{ opacity: 0, y: -10, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: -10, scale: 0.95 }}
                  className="absolute right-0 top-full mt-3 w-56 bg-white/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-white/20 py-3 z-50"
                >
                  <div className="px-4 py-3 border-b border-gray-100/50">
                    <p className="text-sm font-semibold text-gray-900">
                      {session.user?.name || 'User'}
                    </p>
                    <p className="text-xs text-gray-500">
                      {session.user?.email}
                    </p>
                  </div>
                  <motion.button
                    whileHover={{ backgroundColor: '#fef2f2' }}
                    whileTap={{ scale: 0.98 }}
                    onClick={async () => {
                      console.log('Sign out clicked')
                      setIsSigningOut(true)
                      setShowUserMenu(false)
                      try {
                        await signOut({ callbackUrl: '/' })
                      } catch (error) {
                        console.error('Sign out error:', error)
                        setIsSigningOut(false)
                      }
                    }}
                    disabled={isSigningOut}
                    className="w-full px-4 py-3 text-left text-sm text-gray-700 hover:bg-red-50 flex items-center gap-3 disabled:opacity-50 transition-colors"
                  >
                    <LogOut className="w-4 h-4 text-red-500" />
                    {isSigningOut ? 'Signing out...' : 'Sign Out'}
                  </motion.button>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        )}
      </motion.div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-gradient-to-b from-white/40 via-pink-50/20 to-purple-50/20">
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
                stiffness: 100
              }}
            >
              <ChatMessageComponent message={message} />
            </motion.div>
          ))}
        </AnimatePresence>
        
        {/* Loading indicator */}
        {isLoading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="flex gap-4 p-4"
          >
            <motion.div 
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              className="flex-shrink-0"
            >
              <div className="w-10 h-10 rounded-2xl bg-gradient-to-r from-pink-500 via-purple-500 to-pink-600 flex items-center justify-center shadow-lg">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
            </motion.div>
            <div className="flex-1 max-w-3xl">
              <motion.div 
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="inline-block p-6 rounded-3xl bg-white/90 backdrop-blur-sm border border-white/20 shadow-xl"
              >
                <div className="flex items-center gap-3">
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 1.5, repeat: Infinity }}
                    className="w-2 h-2 bg-pink-500 rounded-full"
                  />
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 1.5, repeat: Infinity, delay: 0.2 }}
                    className="w-2 h-2 bg-purple-500 rounded-full"
                  />
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 1.5, repeat: Infinity, delay: 0.4 }}
                    className="w-2 h-2 bg-pink-500 rounded-full"
                  />
                  <span className="text-sm font-medium text-gray-600">Curi is thinking...</span>
                </div>
              </motion.div>
            </div>
          </motion.div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="p-6 border-t border-white/20 bg-white/90 backdrop-blur-xl"
      >
        <div className="flex gap-3 shadow-2xl rounded-2xl bg-white/80 backdrop-blur-sm border border-white/20 px-4 py-3">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me about beauty products..."
            className="flex-1 bg-transparent border-none focus:ring-0 text-base placeholder-gray-400"
            disabled={isLoading}
          />
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleSendMessage}
            disabled={!input.trim() || isLoading}
            className="w-12 h-12 rounded-xl bg-gradient-to-r from-pink-500 via-purple-500 to-pink-600 hover:from-pink-600 hover:via-purple-600 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg flex items-center justify-center transition-all duration-200"
          >
            <Send className="w-5 h-5 text-white" />
          </motion.button>
        </div>
        
        {/* Quick suggestions */}
        {messages.length === 0 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="mt-6"
          >
            <p className="text-sm text-gray-500 mb-3 font-medium">Try asking:</p>
            <div className="flex flex-wrap gap-3">
              {[
                "Find me a good moisturizer for dry skin",
                "What are the best lipsticks under $20?",
                "Recommend anti-aging products for sensitive skin",
                "Show me popular foundations"
              ].map((suggestion, index) => (
                <motion.button
                  key={index}
                  whileHover={{ scale: 1.05, y: -2 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setInput(suggestion)}
                  className="text-sm px-4 py-2 rounded-xl bg-gradient-to-r from-pink-100/80 to-purple-100/80 hover:from-pink-200 hover:to-purple-200 text-pink-700 font-medium shadow-md border border-pink-200/50 transition-all duration-200 backdrop-blur-sm"
                >
                  {suggestion}
                </motion.button>
              ))}
            </div>
          </motion.div>
        )}
      </motion.div>
    </div>
  )
} 