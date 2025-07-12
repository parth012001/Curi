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
      whileHover={{ y: -4, scale: 1.03 }}
      className={cn(
        "rounded-2xl border p-4 shadow-md hover:shadow-lg transition-all duration-200",
        isHighlighted 
          ? "bg-gradient-to-br from-yellow-50 via-orange-50 to-yellow-100 border-yellow-200 shadow-yellow-200/50"
          : "bg-gradient-to-br from-white via-pink-50 to-purple-50 border-gray-100"
      )}
    >
      <div className="space-y-3">
        {/* Product Title */}
        <h3 className={cn(
          "font-semibold text-base line-clamp-2",
          isHighlighted ? "text-gray-900" : "text-gray-900"
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
            isHighlighted ? "text-orange-600" : "text-green-600"
          )}>
            {product?.price ? `$${product.price.toFixed(2)}` : 'Price not available'}
          </span>
          <button className={cn(
            "p-2 rounded-full transition-colors shadow",
            isHighlighted 
              ? "bg-orange-100 hover:bg-orange-200" 
              : "bg-pink-100 hover:bg-pink-200"
          )}>
            <ShoppingBag className={cn(
              "w-5 h-5",
              isHighlighted ? "text-orange-600" : "text-pink-600"
            )} />
          </button>
        </div>
        
        {/* Category */}
        <div className="text-xs text-purple-400 mt-2">
          {product?.main_category || 'Beauty & Personal Care'}
        </div>

        {/* LLM Analysis Score for highlighted products */}
        {isHighlighted && product?.llm_analysis?.match_score && (
          <div className="mt-2 p-2 bg-orange-100 rounded-lg">
            <div className="text-xs text-orange-800 font-medium">
              Match Score: {Math.min(100, Math.max(0, Math.round(product.llm_analysis.match_score * 100)))}%
            </div>
          </div>
        )}
      </div>
    </motion.div>
  )
} 