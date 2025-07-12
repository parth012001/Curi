"use client"

import { motion } from "framer-motion"
import { Lightbulb } from "lucide-react"
import { cn } from "@/lib/utils"

interface InsightBadgeProps {
  insight: string
}

export function InsightBadge({ insight }: InsightBadgeProps) {
  const isNegative = insight.toLowerCase().includes('poor') || 
                     insight.toLowerCase().includes('bad') || 
                     insight.toLowerCase().includes('negative') ||
                     insight.toLowerCase().includes('disappointing') ||
                     insight.toLowerCase().includes('expensive')

  return (
    <motion.div
      whileHover={{ scale: 1.08 }}
      className={cn(
        "inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold shadow-sm border transition-all duration-150",
        isNegative
          ? "bg-gradient-to-r from-red-100 to-pink-100 text-red-700 border-red-200"
          : "bg-gradient-to-r from-green-100 to-purple-100 text-green-700 border-green-200"
      )}
    >
      <Lightbulb className="w-3 h-3" />
      {insight}
    </motion.div>
  )
} 