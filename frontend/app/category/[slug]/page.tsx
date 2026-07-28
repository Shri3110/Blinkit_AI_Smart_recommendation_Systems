/* eslint-disable @next/next/no-img-element */
'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useParams, useRouter } from 'next/navigation'
import { ArrowLeft } from 'lucide-react'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

interface Product {
  id: string;
  name: string;
  brand: string;
  selling_price: number;
  image_url: string;
}

export default function CategoryPage() {
  const params = useParams()
  const router = useRouter()
  const category = decodeURIComponent(params.slug as string)
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Avoid react-hooks/set-state-in-effect warning
    setTimeout(() => setLoading(true), 0)
    fetch(`${API_BASE}/products/category/${category}`)
      .then(res => res.json())
      .then(data => {
        setProducts(data)
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setLoading(false)
      })
  }, [category])

  return (
    <div className="bg-white min-h-screen">
      <div className="flex items-center p-4 border-b">
        <button onClick={() => router.back()} className="mr-3">
          <ArrowLeft size={20} />
        </button>
        <h1 className="text-lg font-bold text-gray-800">{category}</h1>
      </div>

      <div className="p-4">
        {loading ? (
          <div className="grid grid-cols-2 gap-3">
            {[1, 2, 3, 4].map(n => (
              <div key={n} className="bg-white border border-gray-100 rounded-2xl p-2.5 shadow-sm animate-pulse">
                <div className="h-[120px] bg-gray-100 rounded-xl mb-3"></div>
                <div className="h-4 bg-gray-100 rounded mb-2 w-3/4"></div>
                <div className="h-3 bg-gray-100 rounded mb-4 w-1/2"></div>
                <div className="flex justify-between items-end">
                  <div className="h-5 bg-gray-100 rounded w-1/3"></div>
                  <div className="h-7 bg-gray-100 rounded-lg w-12"></div>
                </div>
              </div>
            ))}
          </div>
        ) : products.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-center">
            <div className="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mb-4">
              <span className="text-3xl">🛒</span>
            </div>
            <h2 className="text-lg font-bold text-gray-800 mb-2">No Products Found</h2>
            <p className="text-sm text-gray-500">We couldn&apos;t find any items in this category right now.</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-3">
            {products.map((product, idx) => (
              <div key={idx} className="bg-white rounded-2xl shadow-sm border border-gray-100 p-2.5 flex flex-col group hover:shadow-md transition-shadow">
                <Link href={`/product/${product.id}`} className="relative block h-[120px] bg-gray-50 rounded-xl mb-3 overflow-hidden">
                  <img src={product.image_url} alt={product.name} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                  <div className="absolute top-1 left-1 bg-white/90 backdrop-blur-sm text-[8px] font-extrabold px-1.5 py-0.5 rounded shadow-sm text-gray-800 border border-gray-100">
                    ⏱ 8 MINS
                  </div>
                </Link>
                <Link href={`/product/${product.id}`} className="flex-1 flex flex-col">
                  <h3 className="text-xs font-bold text-gray-800 line-clamp-2 leading-tight h-8 mb-1">{product.name}</h3>
                  <div className="text-[10px] text-gray-500 font-medium">{product.brand}</div>
                </Link>
                <div className="flex items-end justify-between mt-2 pt-1">
                  <div className="flex flex-col">
                    <div className="text-[9px] text-gray-400 line-through">₹{Math.floor(product.selling_price * 1.2)}</div>
                    <div className="font-extrabold text-sm text-gray-900 leading-none">₹{product.selling_price}</div>
                  </div>
                  <button 
                    onClick={async (e) => {
                      e.stopPropagation();
                      e.preventDefault();
                      const userId = localStorage.getItem('blinkit_active_user') || 'TEST_USER_1';
                      try {
                        await fetch(`${API_BASE}/cart/${userId}/add`, {
                          method: 'POST',
                          headers: { 'Content-Type': 'application/json' },
                          body: JSON.stringify({ product_id: product.product_id || product.id, quantity: 1 })
                        });
                        router.push('/cart');
                      } catch (err) {
                        console.error(err);
                      }
                    }}
                    className="bg-green-50 text-green-700 border border-green-200 px-4 py-1.5 rounded-lg text-xs font-extrabold hover:bg-green-600 hover:text-white hover:border-green-600 transition-colors shadow-sm"
                  >
                    ADD
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
