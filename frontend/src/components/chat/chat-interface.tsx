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
    <div className="flex justify-center items-center min-h-[calc(100vh-80px)] w-full px-2 md:px-0">
      <div className="w-full max-w-3xl flex flex-col h-[90vh] glass overflow-hidden">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-transparent">
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
                    ? 'flex justify-end'
                    : 'flex justify-start'
                }
              >
                <div
                  className={
                    message.role === 'user'
                      ? 'glass bg-primary/80 text-white rounded-2xl px-5 py-3 max-w-[80%] shadow-lg border border-white/30'
                      : 'glass bg-white/60 text-text rounded-2xl px-5 py-3 max-w-[80%] shadow-md border border-white/20'
                  }
                  style={{ fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif' }}
                >
                  <ChatMessageComponent message={message} />
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="p-4 border-t border-white/20 glass flex items-center gap-3">
          <Input
            className="flex-1 glass bg-white/70 border border-white/30 rounded-lg px-4 py-2 text-text focus:outline-primary"
            placeholder="Type your message..."
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            disabled={isLoading}
            autoFocus
          />
          <Button
            onClick={handleSendMessage}
            disabled={isLoading || !input.trim()}
            className="bg-primary text-white font-semibold px-6 py-2 rounded-lg shadow-lg hover:bg-secondary transition-colors border-none"
          >
            {isLoading ? <Loader2 className="animate-spin w-5 h-5" /> : <Send className="w-5 h-5" />}
          </Button>
        </div>
      </div>
    </div>
  )
} 