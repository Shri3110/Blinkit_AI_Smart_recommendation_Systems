/* eslint-disable @next/next/no-img-element */
'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Info, ChevronDown, ChevronUp, ShoppingBag } from 'lucide-react'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

const CATEGORY_IMAGES: Record<string, string> = {
  'Fruits & Vegetables': 'https://images.unsplash.com/photo-1610832958506-aa56368176cf?w=400&q=80',
  'Dairy, Bread & Eggs': 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&q=80',
  'Atta, Rice & Dal': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&q=80',
  'Oil & Ghee': 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&q=80',
  'Masalas & Spices': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&q=80',
  'Breakfast & Instant Food': 'https://images.unsplash.com/photo-1504754524776-8f4f37790ca0?w=400&q=80',
  'Snacks & Munchies': 'https://images.unsplash.com/photo-1599490659213-e2b9527bd087?w=400&q=80',
  'Biscuits & Bakery': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400&q=80',
  'Chocolates & Desserts': 'https://images.unsplash.com/photo-1614088685112-0a760b71a3c8?w=400&q=80',
  'Tea & Coffee': 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&q=80',
  'Cold Drinks & Juices': 'https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=400&q=80',
  'Personal Care': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400&q=80',
  'Hair Care': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400&q=80',
  'Skin Care': 'https://images.unsplash.com/photo-1617897903246-719242758050?w=400&q=80',
  'Baby Care': 'https://images.unsplash.com/photo-1519689680058-324335c77eba?w=400&q=80',
  'Pet Care': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400&q=80',
  'Cleaning Essentials': 'https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=400&q=80',
  'Home & Kitchen': 'https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=400&q=80',
  'Ice Cream & Frozen Foods': 'https://images.unsplash.com/photo-1497034825429-c343d7c6a68f?w=400&q=80',
  'Health & Wellness': '/health_wellness.png',
  'Stationery': 'https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=400&q=80',
  'Electronics & Accessories': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400&q=80'
}

interface Product {
  id: string;
  product_id?: string;
  name: string;
  brand: string;
  category: string;
  selling_price: number;
  image_url: string;
}

export default function Home() {
  const router = useRouter()
  const [showSplash, setShowSplash] = useState(true)
  const [categories, setCategories] = useState<string[]>([])
  const [featured, setFeatured] = useState<Product[]>([])
  const [users, setUsers] = useState<any[]>([])
  const [activeUser, setActiveUser] = useState<any>(null)
  const [purchases, setPurchases] = useState<any[]>([])
  const [showHistory, setShowHistory] = useState(false)
  const [showInfo, setShowInfo] = useState(false)
  const [loadingContent, setLoadingContent] = useState(true)
  const [showCatalogueToast, setShowCatalogueToast] = useState(false)

  const fetchPersonalizedContent = async (userId: string) => {
    setLoadingContent(true)
    try {
      const [catRes, featRes] = await Promise.all([
        fetch(`${API_BASE}/categories?user_id=${userId}`),
        fetch(`${API_BASE}/products/featured?user_id=${userId}`)
      ])
      
      if (!catRes.ok) throw new Error(`Categories API failed: ${catRes.status}`)
      if (!featRes.ok) throw new Error(`Featured API failed: ${featRes.status}`)
      
      const cats = await catRes.json()
      const feats = await featRes.json()
      
      setCategories(Array.isArray(cats) ? cats : [])
      setFeatured(Array.isArray(feats) ? feats : [])
    } catch (err) {
      console.error("fetchPersonalizedContent Error:", err)
      setCategories([])
      setFeatured([])
    } finally {
      setLoadingContent(false)
    }
  }

  const addToCart = async (e: React.MouseEvent, productId: string) => {
    e.preventDefault();
    const userId = localStorage.getItem('blinkit_active_user') || 'TEST_USER_1';
    try {
      await fetch(`${API_BASE}/cart/${userId}/add`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId, quantity: 1 })
      });
      router.push('/cart');
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    // Hide splash screen after 1.5 seconds
    const timer = setTimeout(() => {
      setShowSplash(false)
    }, 1500)
    return () => clearTimeout(timer)
  }, [])

  useEffect(() => {
    if (!showSplash) {
        
      // Fetch users for Demo Mode
      fetch(`${API_BASE}/users`)
        .then(res => {
          if (!res.ok) throw new Error(`Users API failed: ${res.status}`)
          return res.json()
        })
        .then(data => {
          if (!Array.isArray(data)) throw new Error("Users API returned non-array")
          setUsers(data)
          const savedUserId = localStorage.getItem('blinkit_active_user')
          if (savedUserId) {
            const user = data.find((u: any) => u.user_id === savedUserId)
            if (user) {
              setActiveUser(user)
              fetchUserPurchases(savedUserId)
              fetchPersonalizedContent(savedUserId)
            } else if (data.length > 0) {
              handleUserChange(data[0])
            } else {
              setLoadingContent(false)
            }
          } else if (data.length > 0) {
            handleUserChange(data[0])
          } else {
            setLoadingContent(false)
          }
        })
        .catch(err => {
          console.error("Failed to fetch API:", err)
          setLoadingContent(false)
        })
    }
  }, [showSplash])

  const fetchUserPurchases = (userId: string) => {
    fetch(`${API_BASE}/users/${userId}/purchases`)
      .then(res => {
        if (!res.ok) throw new Error(`Purchases API failed: ${res.status}`)
        return res.json()
      })
      .then(data => setPurchases(Array.isArray(data) ? data : []))
      .catch(err => {
        console.error("fetchUserPurchases Error:", err)
        setPurchases([])
      })
  }

  const handleUserChange = (user: any) => {
    setActiveUser(user)
    setPurchases([])
    setCategories([])
    setFeatured([])
    localStorage.setItem('blinkit_active_user', user.user_id)
    window.dispatchEvent(new Event('personaChanged'))
    fetchUserPurchases(user.user_id)
    fetchPersonalizedContent(user.user_id)
  }

  if (showSplash) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-yellow-400">
        <div className="text-center animate-pulse">
          <h1 className="text-5xl font-extrabold text-white tracking-tighter">blinkit</h1>
          <p className="text-yellow-800 mt-2 text-sm font-semibold tracking-widest uppercase">Smart Discovery MVP</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-4 pt-20 pb-24 space-y-6">
      
      {/* AI Demo Mode Card */}
      {activeUser && (
        <section className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-4 border border-green-100 shadow-sm relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-green-200 rounded-full blur-3xl opacity-30 -mr-10 -mt-10 pointer-events-none"></div>
          
          <div className="flex justify-between items-center mb-4 relative z-10">
            <h2 className="text-sm font-extrabold text-green-900 tracking-tight flex items-center">
              🤖 Blinkit Smart Discovery Demo
              <button onClick={() => setShowInfo(true)} className="ml-2 text-green-600 hover:text-green-800">
                <Info size={16} />
              </button>
            </h2>
            <select 
              className="bg-white border border-green-200 rounded-lg py-1.5 px-2 text-xs font-bold text-green-900 focus:outline-none shadow-sm cursor-pointer"
              value={activeUser.user_id}
              onChange={(e) => {
                const u = users.find(u => u.user_id === e.target.value);
                if (u) handleUserChange(u);
              }}
            >
              {users.map(u => (
                <option key={u.user_id} value={u.user_id}>{u.name} - {u.occupation}</option>
              ))}
            </select>
          </div>

          <div className="bg-white/80 backdrop-blur-md rounded-xl p-4 border border-white shadow-sm relative z-10 flex gap-4">
            <img src={activeUser.avatar} alt={activeUser.name} className="w-16 h-16 rounded-full border-2 border-green-200 object-cover shadow-sm shrink-0" />
            <div className="flex-1 min-w-0">
              <h3 className="font-extrabold text-gray-900 truncate">{activeUser.name}</h3>
              <p className="text-xs text-gray-600 font-medium mb-2">{activeUser.age} yrs • {activeUser.occupation}</p>
              
              <div className="grid grid-cols-2 gap-2 mb-2">
                <div className="bg-gray-50 rounded p-1.5 border border-gray-100">
                  <span className="block text-[9px] text-gray-500 uppercase tracking-wide font-bold">Behaviour</span>
                  <span className="text-xs font-semibold text-gray-800">{activeUser.shopping_behaviour}</span>
                </div>
                <div className="bg-gray-50 rounded p-1.5 border border-gray-100">
                  <span className="block text-[9px] text-gray-500 uppercase tracking-wide font-bold">Exploration</span>
                  <span className="text-xs font-semibold text-gray-800">{activeUser.exploration_score}/10</span>
                </div>
                <div className="bg-gray-50 rounded p-1.5 border border-gray-100">
                  <span className="block text-[9px] text-gray-500 uppercase tracking-wide font-bold">Avg. Order</span>
                  <span className="text-xs font-semibold text-gray-800">₹{activeUser.average_order_value}</span>
                </div>
                <div className="bg-gray-50 rounded p-1.5 border border-gray-100">
                  <span className="block text-[9px] text-gray-500 uppercase tracking-wide font-bold">Orders/Mo</span>
                  <span className="text-xs font-semibold text-gray-800">{activeUser.monthly_orders}</span>
                </div>
              </div>

              <div className="bg-green-50/50 rounded p-1.5 border border-green-100/50">
                <span className="block text-[9px] text-green-700 uppercase tracking-wide font-bold mb-0.5">Top Categories</span>
                <div className="flex flex-wrap gap-1">
                  {activeUser.favourite_categories?.map((cat: string, i: number) => (
                    <span key={i} className="text-[9px] bg-white border border-green-200 text-green-800 px-1.5 py-0.5 rounded-sm font-semibold">{cat}</span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="mt-3 relative z-10">
            <button 
              onClick={() => setShowHistory(!showHistory)}
              className="w-full flex items-center justify-between bg-white border border-green-100 rounded-lg px-3 py-2 text-xs font-bold text-gray-700 shadow-sm hover:bg-gray-50 transition-colors"
            >
              <span className="flex items-center gap-1.5"><ShoppingBag size={14} className="text-green-600" /> Recent Purchase History</span>
              {showHistory ? <ChevronUp size={16} className="text-gray-400" /> : <ChevronDown size={16} className="text-gray-400" />}
            </button>
            
            {showHistory && (
              <div className="mt-2 bg-white rounded-lg border border-gray-100 p-2 shadow-sm max-h-48 overflow-y-auto">
                {purchases.length === 0 ? (
                  <p className="text-xs text-gray-500 text-center py-4">No recent purchases found.</p>
                ) : (
                  <div className="space-y-2">
                    {purchases.slice(0, 10).map((p, idx) => (
                      <div key={idx} className="flex items-center justify-between text-xs p-1.5 hover:bg-gray-50 rounded">
                        <div className="flex items-center gap-2">
                          <span className="text-[10px] text-gray-400 font-mono w-4">{idx + 1}.</span>
                          <span className="font-semibold text-gray-700 truncate max-w-[120px]">{p.name || 'Product'}</span>
                        </div>
                        <span className="text-gray-500 font-medium">₹{p.price_paid}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </section>
      )}

      {/* Info Modal */}
      {showInfo && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl p-6 max-w-sm w-full shadow-2xl relative">
            <div className="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center mb-4 mx-auto">
              <Info size={24} className="text-blue-500" />
            </div>
            <h3 className="text-lg font-extrabold text-center text-gray-900 mb-2">About Blinkit Smart Discovery Demo</h3>
            <p className="text-sm text-gray-600 text-center mb-6 leading-relaxed">
              This application uses predefined customer personas to simulate different shopping behaviours and demonstrate how the AI recommendation engine personalizes product recommendations. In a real Blinkit application, these insights would be generated automatically from each user&apos;s purchase history.
            </p>
            <button 
              onClick={() => setShowInfo(false)}
              className="w-full bg-gray-900 text-white font-bold py-3 rounded-xl shadow-lg hover:bg-black transition-colors"
            >
              Got it
            </button>
          </div>
        </div>
      )}

      {/* Categories Grid */}
      <section>
        <h2 className="text-lg font-extrabold text-gray-800 mb-4 tracking-tight">Shop by Category</h2>
        <div className="grid grid-cols-4 gap-x-2 gap-y-4">
          {loadingContent ? (
            Array.from({ length: 8 }).map((_, idx) => (
              <div key={idx} className="flex flex-col items-center">
                <div className="w-16 h-16 sm:w-20 sm:h-20 bg-gray-200 animate-pulse rounded-2xl mb-2"></div>
                <div className="h-2 w-10 bg-gray-200 animate-pulse rounded"></div>
              </div>
            ))
          ) : (
            Array.isArray(categories) && categories.slice(0, 8).map((cat, idx) => (
              <Link key={idx} href={`/category/${cat}`} className="flex flex-col items-center group">
                <div className="w-16 h-16 sm:w-20 sm:h-20 bg-blue-50 rounded-2xl flex items-center justify-center mb-2 overflow-hidden relative shadow-sm border border-gray-100 group-hover:shadow-md group-hover:scale-105 transition-all duration-300">
                  {CATEGORY_IMAGES[cat] ? (
                    <img src={CATEGORY_IMAGES[cat]} alt={cat} className="w-full h-full object-cover" />
                  ) : (
                    <div className="text-blue-500 font-bold text-xs text-center px-1">{cat.substring(0, 3).toUpperCase()}</div>
                  )}
                </div>
                <span className="text-[10px] sm:text-xs text-center font-semibold text-gray-700 leading-tight px-1 group-hover:text-green-600 transition-colors">{cat}</span>
              </Link>
            ))
          )}
        </div>
      </section>

      {/* Featured Products Scroll */}
      <section>
        <h2 className="text-lg font-extrabold text-gray-800 mb-4 tracking-tight flex items-center justify-between">
          <span>Featured Products</span>
          <span 
            onClick={() => {
              setShowCatalogueToast(true)
              setTimeout(() => setShowCatalogueToast(false), 4000)
            }}
            className="text-xs font-bold text-green-600 cursor-pointer hover:underline"
          >
            See all
          </span>
        </h2>
        <div className="flex overflow-x-auto space-x-3 pb-4 -mx-4 px-4 scrollbar-hide">
          {loadingContent ? (
            Array.from({ length: 4 }).map((_, idx) => (
              <div key={idx} className="flex-none w-[140px] bg-white rounded-2xl shadow-sm border border-gray-100 p-2.5 flex flex-col">
                <div className="h-[120px] bg-gray-200 animate-pulse rounded-xl mb-3"></div>
                <div className="h-4 bg-gray-200 animate-pulse rounded mb-1"></div>
                <div className="h-3 bg-gray-200 animate-pulse rounded mb-3 w-2/3"></div>
                <div className="flex justify-between items-end mt-auto pt-1">
                  <div className="h-4 bg-gray-200 animate-pulse rounded w-10"></div>
                  <div className="h-6 w-12 bg-gray-200 animate-pulse rounded-lg"></div>
                </div>
              </div>
            ))
          ) : (
            Array.isArray(featured) && featured.map((product, idx) => (
              <div key={idx} className="flex-none w-[140px] bg-white rounded-2xl shadow-sm border border-gray-100 p-2.5 flex flex-col group hover:shadow-md transition-shadow">
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
                    onClick={(e) => { e.stopPropagation(); e.preventDefault(); addToCart(e, product.product_id || product.id); }}
                    className="bg-green-600 text-white border border-green-700 px-4 py-1.5 rounded-lg text-xs font-extrabold hover:bg-green-700 transition-colors shadow-md shadow-green-600/20"
                  >
                    ADD
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </section>
      
      {showCatalogueToast && (
        <div className="fixed top-24 left-1/2 transform -translate-x-1/2 w-11/12 max-w-sm bg-gray-900 text-white text-xs p-3 rounded-lg shadow-xl z-50 animate-fade-in-up">
          <div className="flex items-start">
            <Info size={16} className="text-blue-400 mr-2 flex-shrink-0 mt-0.5" />
            <div className="space-y-2">
              <p className="font-bold">This feature is intentionally out of scope for this MVP.</p>
              <p>The primary objective of this prototype is to validate Blinkit&apos;s AI-powered Smart Discovery recommendation experience during checkout and its ability to encourage cross-category product discovery.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
