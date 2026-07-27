'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { CheckCircle2, TrendingUp, Sparkles, ArrowRight } from 'lucide-react'

/* eslint-disable @next/next/no-img-element */

interface RecommendedProduct {
  name: string;
  image_url: string;
  selling_price: number;
}

interface Stats {
  accepted: boolean;
  aov_increase_estimate: number;
  category: string;
  is_new_category?: boolean;
  recommended_product: RecommendedProduct;
}

export default function SuccessPage() {
  const router = useRouter()
  const [stats, setStats] = useState<Stats | null>(null)

  useEffect(() => {
    const savedStats = localStorage.getItem('blinkit_checkout_stats')
    if (savedStats) {
      // setTimeout to avoid react-hooks/set-state-in-effect warning if it thinks we shouldn't sync update
      setTimeout(() => setStats(JSON.parse(savedStats)), 0)
    }
  }, [])

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col pb-10">
      {/* Top Banner */}
      <div className="bg-green-600 text-white pt-16 pb-8 px-6 text-center shadow-md relative overflow-hidden">
        <div className="absolute -top-10 -right-10 w-32 h-32 bg-green-500 rounded-full opacity-50 blur-2xl"></div>
        <div className="absolute top-10 -left-10 w-24 h-24 bg-green-400 rounded-full opacity-50 blur-xl"></div>
        
        <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg relative z-10 animate-in zoom-in duration-300">
          <CheckCircle2 size={40} className="text-green-600" />
        </div>
        
        <h1 className="text-3xl font-extrabold mb-1 tracking-tight relative z-10">Order Placed!</h1>
        <p className="text-green-100 font-medium relative z-10">Delivery in 10 minutes</p>
      </div>

      <div className="px-4 -mt-4 relative z-20 space-y-4">
        
        {/* Dashboard Title */}
        <div className="text-center pt-6 pb-2">
          <div className="inline-flex items-center space-x-2 bg-yellow-100 text-yellow-900 px-3 py-1.5 rounded-full text-[10px] font-extrabold uppercase tracking-widest mb-2 border border-yellow-200 shadow-sm">
            <Sparkles size={14} className="fill-current" />
            <span>Blinkit Smart Discovery Summary</span>
          </div>
        </div>

        {stats ? (
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden animate-in slide-in-from-bottom-5 duration-500">
            {/* Status Header */}
            <div className="bg-gray-50 border-b border-gray-100 p-4 flex items-center justify-between">
              <div className="text-sm font-bold text-gray-700">Recommendation Status</div>
              {stats.accepted ? (
                <div className="bg-green-100 text-green-700 text-xs font-bold px-3 py-1 rounded-full flex items-center">
                  <CheckCircle2 size={12} className="mr-1" /> Accepted
                </div>
              ) : (
                <div className="bg-gray-200 text-gray-600 text-xs font-bold px-3 py-1 rounded-full">
                  ✗ Skipped
                </div>
              )}
            </div>
            
            <div className="p-5">
              {stats.accepted && stats.recommended_product ? (
                <>
                  <div className="space-y-3 mb-5">
                    <div className="flex items-center text-sm font-semibold text-gray-800">
                      <CheckCircle2 size={16} className="text-green-600 mr-2 flex-shrink-0" />
                      Recommendation Accepted
                    </div>
                    <div className="flex items-center text-sm font-semibold text-gray-800">
                      <CheckCircle2 size={16} className="text-green-600 mr-2 flex-shrink-0" />
                      Category: {stats.category}
                      {stats.is_new_category && (
                        <span className="ml-2 text-[10px] font-extrabold text-green-700 bg-green-100 px-2 py-0.5 rounded-full border border-green-300 uppercase tracking-wider flex items-center">
                          <span className="mr-1">🟢</span> NEW CATEGORY
                        </span>
                      )}
                    </div>
                    <div className="flex items-center text-sm font-semibold text-gray-800">
                      <CheckCircle2 size={16} className="text-green-600 mr-2 flex-shrink-0" />
                      Recommended Product: {stats.recommended_product.name}
                    </div>
                    <div className="flex items-start text-sm font-semibold text-gray-800">
                      <CheckCircle2 size={16} className="text-green-600 mr-2 flex-shrink-0 mt-0.5" />
                      {stats.is_new_category 
                        ? "Thanks for exploring a new category! We'll use your shopping preferences to make future recommendations even more relevant."
                        : "We'll continue personalizing recommendations based on your shopping preferences."}
                    </div>
                  </div>
                </>
              ) : (
                <div className="space-y-3 mb-2">
                  <div className="flex items-center text-sm font-semibold text-gray-800">
                    <div className="w-4 h-4 rounded-full bg-gray-200 text-gray-500 flex items-center justify-center text-[10px] mr-2 flex-shrink-0">✗</div>
                    Recommendation Skipped
                  </div>
                  <p className="text-sm text-gray-600 leading-relaxed font-medium">
                    Your order has been placed successfully.
                  </p>
                  <p className="text-sm text-gray-600 leading-relaxed">
                    We'll continue learning from your shopping preferences to make future recommendations more relevant.
                  </p>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 text-center animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-1/2 mx-auto mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-1/3 mx-auto"></div>
          </div>
        )}

        <div className="pt-6">
          <button 
            onClick={() => router.push('/')}
            className="w-full bg-white border border-gray-200 text-gray-800 font-extrabold py-3.5 rounded-xl shadow-sm hover:bg-gray-50 hover:border-gray-300 transition-colors flex items-center justify-center"
          >
            Back to Home
          </button>
        </div>
      </div>
    </div>
  )
}
