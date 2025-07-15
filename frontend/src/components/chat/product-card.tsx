"use client"

import { motion } from "framer-motion"
import { Star, ShoppingBag } from "lucide-react"
import { Product } from "@/lib/utils"
import { cn } from "@/lib/utils"

interface ProductCardProps {
  product: Product | undefined
  isHighlighted?: boolean
}

export function ProductCard({ product, isHighlighted = false }: ProductCardProps) {
  // Early return if no product
  if (!product) {
    return (
      <motion.div
        whileHover={{ y: -4, scale: 1.03 }}
        className="bg-gradient-to-br from-gray-100 to-gray-200 rounded-2xl border border-gray-200 p-4 shadow-md"
      >
        <div className="text-center text-gray-500">
          <p>Product information not available</p>
        </div>
      </motion.div>
    )
  }

  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={cn(
          "w-3 h-3",
          i < Math.floor(rating) 
            ? "fill-yellow-400 text-yellow-400" 
            : "text-gray-300"
        )}
      />
    ))
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 16, scale: 0.97 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: 16, scale: 0.97 }}
      whileHover={{ y: -4, scale: 1.03, boxShadow: '0 12px 40px 0 rgba(31,38,135,0.16)' }}
      whileTap={{ scale: 0.98 }}
      transition={{ type: 'spring', stiffness: 120, damping: 14 }}
      className={cn(
        "glass p-4 shadow-xl hover:shadow-2xl transition-all duration-200 border border-white/30",
        isHighlighted 
          ? "ring-2 ring-primary/40"
          : ""
      )}
    >
      <div className="space-y-3">
        {/* Product Title */}
        <h3 className={cn(
          "font-semibold text-base line-clamp-2 text-text",
          isHighlighted ? "text-primary" : ""
        )}>
          {product?.title || 'Product Title Not Available'}
        </h3>
        
        {/* Brand */}
        <p className="text-xs text-gray-500 mb-1">
          by {product?.store || 'Unknown Brand'}
        </p>
        
        {/* Rating */}
        <div className="flex items-center gap-2">
          <div className="flex items-center">
            {renderStars(product?.average_rating || 0)}
          </div>
          <span className="text-xs text-gray-500">
            {(product?.average_rating || 0).toFixed(1)} ({(product?.rating_number || 0).toLocaleString()})
          </span>
        </div>
        
        {/* Price */}
        <div className="flex items-center justify-between mt-2">
          <span className={cn(
            "font-bold text-lg",
            isHighlighted ? "text-primary" : "text-secondary"
          )}>
            {product?.price ? `$${product.price.toFixed(2)}` : 'Price not available'}
          </span>
          <button className={cn(
            "p-2 rounded-full transition-colors shadow glass border border-white/30",
            isHighlighted 
              ? "bg-primary/10 hover:bg-primary/20" 
              : "bg-secondary/10 hover:bg-secondary/20"
          )}>
            <ShoppingBag className={cn(
              "w-5 h-5",
              isHighlighted ? "text-primary" : "text-secondary"
            )} />
          </button>
        </div>
        
        {/* Category */}
        <div className="text-xs text-primary/70 mt-2">
          {product?.main_category || 'Beauty & Personal Care'}
        </div>

        {/* LLM Analysis Score for highlighted products */}
        {isHighlighted && product?.llm_analysis?.match_score && (
          <div className="mt-2 p-2 bg-primary/10 rounded-lg">
            <div className="text-xs text-primary font-medium">
              Match Score: {Math.min(100, Math.max(0, Math.round(product.llm_analysis.match_score * 100)))}%
            </div>
          </div>
        )}
      </div>
    </motion.div>
  )
} 