"use client"

import { motion } from "framer-motion"
import { Lightbulb, ThumbsUp, AlertTriangle, Star, Users } from "lucide-react"
import { cn } from "@/lib/utils"

interface InsightBadgeProps {
  insight: string
}

export function InsightBadge({ insight }: InsightBadgeProps) {
  const insightLower = insight.toLowerCase()
  
  // Categorize insights
  const isPositive = insightLower.includes('love') || 
                     insightLower.includes('great') || 
                     insightLower.includes('effective') ||
                     insightLower.includes('recommended') ||
                     insightLower.includes('highly') ||
                     insightLower.includes('well-rated') ||
                     insightLower.includes('gentle') ||
                     insightLower.includes('hydrating') ||
                     insightLower.includes('smooth')

  const isNegative = insightLower.includes('poor') || 
                     insightLower.includes('bad') || 
                     insightLower.includes('negative') ||
                     insightLower.includes('disappointing') ||
                     insightLower.includes('expensive') ||
                     insightLower.includes('irritating') ||
                     insightLower.includes('harsh')

  const isRating = insightLower.includes('rated') || 
                   insightLower.includes('stars') ||
                   insightLower.includes('⭐')

  const isUserFeedback = insightLower.includes('users') || 
                         insightLower.includes('mention') ||
                         insightLower.includes('say')

  // Choose appropriate icon and styling
  let icon = <Lightbulb className="w-3 h-3" />
  let bgClass = "bg-gradient-to-r from-blue-100 to-purple-100 text-blue-700 border-blue-200"
  
  if (isPositive) {
    icon = <ThumbsUp className="w-3 h-3" />
    bgClass = "bg-gradient-to-r from-green-100 to-emerald-100 text-green-700 border-green-200"
  } else if (isNegative) {
    icon = <AlertTriangle className="w-3 h-3" />
    bgClass = "bg-gradient-to-r from-red-100 to-pink-100 text-red-700 border-red-200"
  } else if (isRating) {
    icon = <Star className="w-3 h-3" />
    bgClass = "bg-gradient-to-r from-yellow-100 to-orange-100 text-yellow-700 border-yellow-200"
  } else if (isUserFeedback) {
    icon = <Users className="w-3 h-3" />
    bgClass = "bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700 border-purple-200"
  }

  return (
    <motion.div
      whileHover={{ scale: 1.05, y: -2 }}
      className={cn(
        "inline-flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-medium shadow-sm border transition-all duration-200 cursor-pointer",
        bgClass
      )}
    >
      {icon}
      <span className="leading-relaxed">{insight}</span>
    </motion.div>
  )
} 