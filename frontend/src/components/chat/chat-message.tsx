"use client"

import { motion } from "framer-motion"
import { Bot, User } from "lucide-react"
import { ChatMessage, Product } from "@/lib/utils"
import { cn } from "@/lib/utils"
import { ProductCard } from "./product-card"
import { InsightBadge } from "./insight-badge"

interface ChatMessageProps {
  message: ChatMessage
}

export function ChatMessageComponent({ message }: ChatMessageProps) {
  const isUser = message.role === "user"

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={cn(
        "flex gap-3 py-2 px-1",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      {!isUser && (
        <div className="flex-shrink-0">
          <div className="w-8 h-8 rounded-full bg-gradient-to-r from-pink-500 to-purple-600 flex items-center justify-center shadow-md">
            <Bot className="w-4 h-4 text-white" />
          </div>
        </div>
      )}
      <div className={cn(
        "flex-1 max-w-2xl",
        isUser ? "text-right" : "text-left"
      )}>
        <div className={cn(
          "inline-block p-4 rounded-2xl shadow-md",
          isUser 
            ? "bg-gradient-to-r from-pink-500 to-purple-600 text-white rounded-br-3xl rounded-tr-3xl rounded-bl-xl"
            : "bg-white border border-gray-100 text-gray-900 rounded-bl-3xl rounded-tl-3xl rounded-br-xl"
        )}>
          <p className="text-base leading-relaxed whitespace-pre-line">{message.content}</p>
        </div>
        {/* Products */}
        {message.products && message.products.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.3 }}
            className="mt-4 space-y-3"
          >
            <h4 className="text-sm font-semibold text-pink-700 mb-2 tracking-tight">
              📦 Recommended Products
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {message.products.map((product) => (
                <ProductCard key={product.asin} product={product} />
              ))}
            </div>
          </motion.div>
        )}
        {/* Insights */}
        {message.insights && message.insights.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.3 }}
            className="mt-4"
          >
            <h4 className="text-sm font-semibold text-purple-700 mb-2 tracking-tight">
              💡 Key Insights
            </h4>
            <div className="flex flex-wrap gap-2">
              {message.insights.map((insight, index) => (
                <InsightBadge key={index} insight={insight} />
              ))}
            </div>
          </motion.div>
        )}
        {/* Confidence indicator */}
        {message.confidence && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6, duration: 0.3 }}
            className="mt-2 text-xs text-gray-400"
          >
            Confidence: {Math.round(message.confidence * 100)}%
          </motion.div>
        )}
      </div>
      {isUser && (
        <div className="flex-shrink-0">
          <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center shadow">
            <User className="w-4 h-4 text-gray-600" />
          </div>
        </div>
      )}
    </motion.div>
  )
} 