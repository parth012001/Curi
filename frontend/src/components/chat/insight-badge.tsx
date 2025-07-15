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
  let bgClass = "glass border border-white/30 text-primary"
  
  if (isPositive) {
    icon = <ThumbsUp className="w-3 h-3" />
    bgClass = "glass border border-white/30 text-secondary"
  } else if (isNegative) {
    icon = <AlertTriangle className="w-3 h-3" />
    bgClass = "glass border border-white/30 text-error"
  } else if (isRating) {
    icon = <Star className="w-3 h-3" />
    bgClass = "glass border border-white/30 text-yellow-600"
  } else if (isUserFeedback) {
    icon = <Users className="w-3 h-3" />
    bgClass = "glass border border-white/30 text-primary"
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
      whileHover={{ scale: 1.07, y: -2, boxShadow: '0 6px 24px 0 rgba(124,131,253,0.10)' }}
      whileTap={{ scale: 0.97 }}
      transition={{ type: 'spring', stiffness: 180, damping: 18 }}
      className={cn(
        "inline-flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-medium shadow-md transition-all duration-200 cursor-pointer",
        bgClass
      )}
    >
      {icon}
      <span className="leading-relaxed">{insight}</span>
    </motion.div>
  )
} 