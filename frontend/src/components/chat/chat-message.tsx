"use client"

import { motion } from "framer-motion"
import { Bot, User, Star, TrendingUp, Award, Info, CheckCircle } from "lucide-react"
import { ChatMessage, Product } from "@/lib/utils"
import { cn } from "@/lib/utils"
import { ProductCard } from "./product-card"
import { InsightBadge } from "./insight-badge"
import ReactMarkdown from "react-markdown"

interface ChatMessageProps {
  message: ChatMessage
}

export function ChatMessageComponent({ message }: ChatMessageProps) {
  const isUser = message.role === "user"

  // Sort products by relevance (LLM analysis score or similarity score)
  const sortedProducts = message.products?.sort((a, b) => {
    const scoreA = a?.llm_analysis?.match_score || a?.similarity_score || 0
    const scoreB = b?.llm_analysis?.match_score || b?.similarity_score || 0
    return scoreB - scoreA
  }) || []

  const topProduct = sortedProducts[0]
  const otherProducts = sortedProducts.slice(1, 4) // Show top 4 total

  // Helper function to validate and format match score
  const getValidMatchScore = (product: Product | undefined) => {
    if (!product || !product.llm_analysis?.match_score) return null
    
    const score = product.llm_analysis.match_score
    // Ensure score is between 0 and 1 (0-100%)
    const validScore = Math.max(0, Math.min(1, score))
    return validScore
  }

  const topProductMatchScore = getValidMatchScore(topProduct)

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ 
        duration: 0.4,
        type: "spring",
        stiffness: 100
      }}
      className={cn(
        "flex gap-4 py-3 px-2",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      {!isUser && (
        <motion.div 
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: "spring" }}
          className="flex-shrink-0"
        >
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-r from-pink-500 via-purple-500 to-pink-600 flex items-center justify-center shadow-lg">
            <Bot className="w-5 h-5 text-white" />
          </div>
        </motion.div>
      )}
      <div className={cn(
        "flex-1 max-w-4xl",
        isUser ? "text-right" : "text-left"
      )}>
        <motion.div 
          whileHover={{ scale: 1.02 }}
          className={cn(
            "inline-block p-6 rounded-3xl shadow-xl border",
            isUser 
              ? "bg-primary text-white border-white/30 rounded-br-2xl rounded-tr-2xl rounded-bl-xl shadow-lg"
              : "bg-white/90 backdrop-blur-sm border-white/20 text-gray-900 rounded-bl-2xl rounded-tl-2xl rounded-br-xl shadow-lg"
          )}
          style={isUser ? { textShadow: '0 1px 8px rgba(34,34,59,0.18)' } : {}}
        >
          <div className="text-base leading-relaxed">
            <ReactMarkdown 
              components={{
                p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                strong: ({ children }) => <strong className="font-semibold text-gray-900">{children}</strong>,
                em: ({ children }) => <em className="italic text-gray-700">{children}</em>,
                ul: ({ children }) => <ul className="list-disc list-inside space-y-1 my-2">{children}</ul>,
                ol: ({ children }) => <ol className="list-decimal list-inside space-y-1 my-2">{children}</ol>,
                li: ({ children }) => <li className="text-gray-700">{children}</li>,
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        </motion.div>

        {/* Top Recommendation - Highlighted */}
        {topProduct && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.4 }}
            className="mt-6"
          >
            <motion.div
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
              className="flex items-center gap-2 mb-4"
            >
              <div className="flex items-center gap-2 bg-gradient-to-r from-yellow-400 to-orange-500 text-white px-3 py-1 rounded-full text-sm font-semibold shadow-lg">
                <Award className="w-4 h-4" />
                Best Match
              </div>
              {topProductMatchScore && (
                <div className="flex items-center gap-1 text-sm text-gray-600">
                  <TrendingUp className="w-4 h-4 text-green-500" />
                  {Math.round(topProductMatchScore * 100)}% match
                </div>
              )}
            </motion.div>
            
            <motion.div
              whileHover={{ scale: 1.02 }}
              className="relative"
            >
              <div className="absolute -inset-1 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-2xl blur opacity-20"></div>
              <div className="relative bg-white rounded-2xl p-1">
                <ProductCard product={topProduct} isHighlighted={true} />
              </div>
            </motion.div>

            {/* LLM Reasoning for top product */}
            {topProduct.llm_analysis?.reasoning && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="mt-3 p-3 bg-blue-50 rounded-xl border border-blue-200"
              >
                <div className="flex items-start gap-2">
                  <Info className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
                  <div className="text-sm text-blue-800">
                    <span className="font-medium">Why this matches:</span> {topProduct.llm_analysis.reasoning}
                  </div>
                </div>
              </motion.div>
            )}
          </motion.div>
        )}

        {/* Other Recommendations */}
        {otherProducts.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.3 }}
            className="mt-6"
          >
            <motion.h4 
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.7 }}
              className="text-sm font-semibold text-gray-700 mb-4 tracking-tight flex items-center gap-2"
            >
              <span className="text-lg">✨</span>
              More Great Options
            </motion.h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {otherProducts.map((product, index) => (
                <motion.div
                  key={product.asin}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.8 + index * 0.1 }}
                >
                  <ProductCard product={product} />
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {/* Insights Section */}
        {message.insights && message.insights.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.9, duration: 0.3 }}
            className="mt-6"
          >
            <motion.h4 
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 1.0 }}
              className="text-sm font-semibold text-purple-700 mb-3 tracking-tight flex items-center gap-2"
            >
              <span className="text-lg">💡</span>
              Key Insights
            </motion.h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {message.insights.map((insight, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 1.1 + index * 0.1 }}
                >
                  <InsightBadge insight={insight} />
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {/* Confidence and Quality Indicators */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2, duration: 0.3 }}
          className="mt-4 flex items-center justify-between text-xs text-gray-500"
        >
          <div className="flex items-center gap-2">
            <CheckCircle className="w-3 h-3 text-green-500" />
            <span>AI-powered recommendations</span>
          </div>
          {message.confidence && (
            <div className="flex items-center gap-1">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              {Math.round(message.confidence * 100)}% confidence
            </div>
          )}
        </motion.div>
      </div>
      {isUser && (
        <motion.div 
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: "spring" }}
          className="flex-shrink-0"
        >
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-r from-gray-400 to-gray-500 flex items-center justify-center shadow-lg">
            <User className="w-5 h-5 text-white" />
          </div>
        </motion.div>
      )}
    </motion.div>
  )
} 