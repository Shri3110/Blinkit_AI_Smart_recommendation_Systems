/* eslint-disable @next/next/no-img-element */
'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { ArrowLeft, Star, Clock } from 'lucide-react'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

interface Product {
  id: string;
  product_id?: string;
  name: string;
  brand: string;
  subcategory: string;
  description: string;
  selling_price: number;
  mrp: number;
  image_url: string;
}

export default function ProductPage() {
  const params = useParams()
  const router = useRouter()
  const productId = params.id as string
  const [product, setProduct] = useState<Product | null>(null)

  useEffect(() => {
    fetch(`${API_BASE}/products/${productId}`)
      .then(res => res.json())
      .then(data => setProduct(data))
      .catch(err => console.error(err))
  }, [productId])

  if (!product) {
    return (
      <div className="bg-gray-50 min-h-screen">
        <div className="bg-white animate-pulse">
          <div className="h-64 bg-gray-100 w-full"></div>
          <div className="p-4">
            <div className="h-4 bg-gray-100 rounded w-1/4 mb-2"></div>
            <div className="h-8 bg-gray-100 rounded w-3/4 mb-4"></div>
            <div className="h-4 bg-gray-100 rounded w-1/2 mb-6"></div>
            <div className="flex items-center justify-between border-t border-b py-4">
              <div className="h-8 bg-gray-100 rounded w-1/3"></div>
              <div className="h-10 bg-gray-100 rounded-lg w-1/3"></div>
            </div>
            <div className="mt-4 space-y-2">
              <div className="h-4 bg-gray-100 rounded w-full"></div>
              <div className="h-4 bg-gray-100 rounded w-full"></div>
              <div className="h-4 bg-gray-100 rounded w-2/3"></div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-gray-50 min-h-screen">
      <div className="bg-white">
        <div className="absolute top-4 left-4 z-10 bg-white/80 p-2 rounded-full backdrop-blur-sm cursor-pointer shadow-sm" onClick={() => router.back()}>
          <ArrowLeft size={20} />
        </div>
        
        <div className="h-64 bg-gray-100 flex items-center justify-center w-full overflow-hidden">
          <img src={product.image_url} alt={product.name} className="w-full h-full object-cover" />
        </div>

        <div className="p-4">
          <div className="text-xs font-bold text-gray-500 tracking-wider uppercase mb-1">{product.brand}</div>
          <h1 className="text-xl font-bold text-gray-800 leading-tight mb-2">{product.name}</h1>
          <div className="flex items-center text-xs text-gray-500 mb-4 space-x-3">
            <span className="flex items-center"><Clock size={12} className="mr-1"/> 10 MINS</span>
            <span className="bg-gray-100 px-2 py-0.5 rounded flex items-center">
              4.5 <Star size={10} className="ml-1 text-green-600 fill-current"/>
            </span>
          </div>

          <div className="flex items-center justify-between border-t border-b py-4">
            <div>
              <div className="text-2xl font-bold text-gray-900">₹{product.selling_price}</div>
              <div className="text-xs text-gray-500 mt-1">Inclusive of all taxes</div>
            </div>
            <button 
              onClick={async () => {
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
              className="bg-green-600 text-white px-8 py-2 rounded-lg font-bold shadow-md hover:bg-green-700 transition"
            >
              Add to Cart
            </button>
          </div>
          
          <div className="mt-4">
            <h3 className="font-bold text-gray-800 mb-2">Product Details</h3>
            <p className="text-sm text-gray-600 leading-relaxed">
              Experience the best quality {product.subcategory} from {product.brand}. Sourced carefully and delivered fresh to your doorstep in 10 minutes.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
