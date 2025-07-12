import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// API base URL
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// API client
export async function apiCall<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`
  
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    throw new Error(`API call failed: ${response.statusText}`)
  }

  return response.json()
}

// Chat message types
export interface ChatMessage {
  id: string
  content: string
  role: 'user' | 'assistant'
  timestamp: Date
  products?: Product[]
  insights?: string[]
  confidence?: number
}

export interface Product {
  asin: string
  title: string
  store: string
  main_category?: string
  average_rating: number
  rating_number: number
  price?: number
  similarity_score: number
  insights?: string[]
  review_count?: number
  llm_analysis?: {
    match_score: number
    reasoning: string
    key_features: string[]
  }
}

export interface ChatResponse {
  response: string
  products: Product[]
  insights: string[]
  confidence: number
} 