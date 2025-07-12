"use client"

import { motion } from "framer-motion"
import { Star, ShoppingBag } from "lucide-react"
import { Product } from "@/lib/utils"
import { cn } from "@/lib/utils"

interface ProductCardProps {
  product: Product
}

export function ProductCard({ product }: ProductCardProps) {
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
      className="bg-gradient-to-br from-white via-pink-50 to-purple-50 rounded-2xl border border-gray-100 p-4 shadow-md hover:shadow-lg transition-all duration-200"
    >
      <div className="space-y-3">
        {/* Product Title */}
        <h3 className="font-semibold text-base text-gray-900 line-clamp-2">
          {product.title}
        </h3>
        
        {/* Brand */}
        <p className="text-xs text-gray-500 mb-1">
          by {product.store || 'Unknown Brand'}
        </p>
        
        {/* Rating */}
        <div className="flex items-center gap-2">
          <div className="flex items-center">
            {renderStars(product.average_rating || 0)}
          </div>
          <span className="text-xs text-gray-500">
            {(product.average_rating || 0).toFixed(1)} ({(product.rating_number || 0).toLocaleString()})
          </span>
        </div>
        
        {/* Price */}
        <div className="flex items-center justify-between mt-2">
          <span className="font-bold text-lg text-green-600">
            {product.price ? `$${product.price.toFixed(2)}` : 'Price not available'}
          </span>
          <button className="p-2 rounded-full bg-pink-100 hover:bg-pink-200 transition-colors shadow">
            <ShoppingBag className="w-5 h-5 text-pink-600" />
          </button>
        </div>
        
        {/* Category */}
        <div className="text-xs text-purple-400 mt-2">
          {product.main_category || 'Beauty & Personal Care'}
        </div>
      </div>
    </motion.div>
  )
} 