'use client'

import { useState, useEffect } from 'react'
import { Sparkles, X, Plus, Search, Info } from 'lucide-react'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

/* eslint-disable @next/next/no-img-element */

interface Product {
  id: string;
  product_id?: string;
  name: string;
  brand: string;
  category: string;
  selling_price: number;
  image_url: string;
}

interface DiscoveryData {
  recommended_product: Product;
  explanation: string;
  confidence_score: number;
  matched_reasons?: string[];
  is_new_category?: boolean;
}

export default function SmartDiscoveryModal({ userId, activeUser, onSkip, onAccept }: { userId: string, activeUser: Record<string, unknown>, onSkip: (payload?: Record<string, unknown>) => void, onAccept: (payload?: Record<string, unknown>) => void }) {
  const [recommendation, setRecommendation] = useState<DiscoveryData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    fetch(`${API_BASE}/recommend/${userId}`, { method: 'POST' })
      .then(res => {
        if (!res.ok) throw new Error("Failed")
        return res.json()
      })
      .then(data => {
        setRecommendation(data)
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setError(true)
        setLoading(false)
        onSkip() // Fail gracefully
      })
  }, [userId, onSkip])

  const handleSkip = () => {
    if (recommendation && activeUser) {
      localStorage.setItem('blinkit_checkout_stats', JSON.stringify({
        accepted: false,
        recommended_product: recommendation.recommended_product,
        category: recommendation.recommended_product.category,
        is_new_category: recommendation.is_new_category,
        user_aov: activeUser.average_order_value || 0,
        user_exploration_score: activeUser.exploration_score || 0
      }))
    }
    onSkip()
  }

  const handleAccept = () => {
    if (recommendation && activeUser) {
      localStorage.setItem('blinkit_checkout_stats', JSON.stringify({
        accepted: true,
        recommended_product: recommendation.recommended_product,
        category: recommendation.recommended_product.category,
        is_new_category: recommendation.is_new_category,
        user_aov: activeUser.average_order_value || 0,
        user_exploration_score: activeUser.exploration_score || 0
      }))
    }
    onAccept({ product_id: recommendation?.recommended_product?.id })
  }

  if (error) return null

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/60 backdrop-blur-sm p-4 sm:p-0">
      <div className="bg-white w-full max-w-md rounded-t-3xl sm:rounded-3xl shadow-2xl overflow-hidden animate-in slide-in-from-bottom-10 duration-300 max-h-[90vh] flex flex-col">
        
        {loading ? (
          <div className="p-8 flex flex-col items-center justify-center space-y-6">
            <div className="w-16 h-16 rounded-full bg-yellow-100 flex items-center justify-center animate-pulse">
              <Sparkles className="text-yellow-500" size={32} />
            </div>
            <div className="space-y-3 w-full">
              <div className="h-4 bg-gray-200 rounded-full w-3/4 mx-auto animate-pulse"></div>
              <div className="h-4 bg-gray-200 rounded-full w-1/2 mx-auto animate-pulse"></div>
            </div>
          </div>
        ) : recommendation ? (
          <div className="flex flex-col overflow-hidden">
            {/* Header */}
            <div className="flex-shrink-0 bg-gradient-to-r from-yellow-400 to-yellow-500 p-4 text-white relative">
              <button onClick={handleSkip} className="absolute top-4 right-4 bg-black/10 rounded-full p-1 hover:bg-black/20 transition">
                <X size={20} />
              </button>
              <div className="flex items-center space-x-2 mb-1 text-yellow-900">
                <Sparkles size={16} className="fill-current" />
                <span className="font-bold text-xs tracking-wider uppercase">Smart Discovery</span>
              </div>
              <h2 className="text-xl font-extrabold shadow-sm">Recommended for You</h2>
            </div>
            
            {/* Content */}
            <div className="p-5 overflow-y-auto flex-1">
              {/* Disabled Search Bar */}
              <div className="relative group mb-5">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Search size={16} className="text-gray-400" />
                </div>
                <input 
                  type="text" 
                  disabled
                  className="block w-full pl-10 pr-10 py-2.5 border border-gray-200 rounded-xl leading-5 bg-gray-50 placeholder-gray-400 focus:outline-none cursor-not-allowed sm:text-sm transition-all shadow-inner text-gray-400" 
                  placeholder="Search groceries & essentials" 
                />
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center cursor-help">
                  <Info size={16} className="text-gray-400 group-hover:text-blue-500 transition-colors" />
                </div>
                <div className="absolute top-full left-0 mt-2 w-full p-2 bg-gray-900 text-white text-[10px] rounded shadow-xl opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50">
                  Search is intentionally disabled in this MVP to evaluate the impact of AI-driven contextual recommendations without introducing manual exploration.
                </div>
              </div>

              <div className="flex space-x-4 mb-4">
                <div className="w-24 h-24 bg-gray-50 rounded-xl border border-gray-100 flex-shrink-0 flex items-center justify-center overflow-hidden relative shadow-sm">
                  <img src={recommendation.recommended_product.image_url} alt={recommendation.recommended_product.name} className="w-full h-full object-cover" />
                  <div className="absolute top-1 left-1 bg-white/90 backdrop-blur-sm text-[8px] font-extrabold px-1.5 py-0.5 rounded shadow-sm text-gray-800 border border-gray-100">
                    ⏱ 8 MINS
                  </div>
                </div>
                <div className="flex flex-col justify-center">
                  <div className="flex items-center space-x-2 mb-1">
                    <div className="text-[10px] font-extrabold text-green-700 bg-green-50 px-2 py-0.5 rounded-full w-max border border-green-200 uppercase tracking-wider">
                      {recommendation.recommended_product.category as string}
                    </div>
                    {recommendation.is_new_category && (
                      <div className="text-[10px] font-extrabold text-green-700 bg-green-100 px-2 py-0.5 rounded-full w-max border border-green-300 uppercase tracking-wider flex items-center">
                        <span className="mr-1">🟢</span> NEW CATEGORY
                      </div>
                    )}
                  </div>
                  <h3 className="font-bold text-gray-800 leading-tight mb-1">{recommendation.recommended_product.name}</h3>
                  <div className="text-xs text-gray-500 mb-2 font-medium">{recommendation.recommended_product.brand}</div>
                  <div className="font-extrabold text-lg text-gray-900">₹{recommendation.recommended_product.selling_price}</div>
                </div>
              </div>

              <div className="bg-gray-50 p-4 rounded-xl border border-gray-100 mb-5 relative overflow-hidden">
                <div className="absolute top-0 left-0 w-1 h-full bg-yellow-400"></div>
                <h4 className="font-bold text-gray-900 mb-2 text-sm">Matched because</h4>
                {recommendation.matched_reasons && recommendation.matched_reasons.length > 0 && (
                  <ul className="text-xs text-gray-700 space-y-1.5 mb-3">
                    {recommendation.matched_reasons.map((reason, idx) => (
                      <li key={idx} className="flex items-start">
                        <span className="text-green-600 mr-2">✓</span> {reason}
                      </li>
                    ))}
                  </ul>
                )}
                <p className="text-xs text-gray-700 leading-relaxed italic">
                  &quot;{recommendation.explanation}&quot;
                </p>
                <div className="mt-3 flex items-center justify-between text-xs">
                  <span className="text-gray-500 font-medium">Recommendation Match</span>
                  <span className="font-bold text-green-600 flex items-center bg-green-50 px-2 py-0.5 rounded-full">
                    {recommendation.confidence_score}% Match
                  </span>
                </div>
              </div>

              {/* Actions */}
              <div className="grid grid-cols-2 gap-3">
                <button 
                  onClick={handleSkip}
                  className="py-3.5 rounded-xl font-bold text-gray-600 bg-gray-100 hover:bg-gray-200 transition-colors"
                >
                  No Thanks
                </button>
                <button 
                  onClick={handleAccept}
                  className="py-3.5 rounded-xl font-extrabold text-white bg-green-600 shadow-lg shadow-green-600/20 hover:bg-green-700 transition-all flex items-center justify-center"
                >
                  <Plus size={18} className="mr-1" /> Add to Cart
                </button>
              </div>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  )
}
