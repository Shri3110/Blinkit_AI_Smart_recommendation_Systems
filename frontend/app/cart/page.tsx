/* eslint-disable @next/next/no-img-element, @typescript-eslint/no-explicit-any, @typescript-eslint/no-unused-vars, jsx-a11y/alt-text */
'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { ArrowLeft, ShoppingBag, MapPin, Clock, CreditCard, Receipt, Trash2 } from 'lucide-react'
import SmartDiscoveryModal from '@/components/SmartDiscoveryModal'

const API_BASE = 'http://localhost:8000/api'

export default function CartPage() {
  const router = useRouter()
  const [users, setUsers] = useState<any[]>([])
  const [selectedUserId, setSelectedUserId] = useState('')
  const [cart, setCart] = useState<any>(null)
  const [purchases, setPurchases] = useState<any[]>([])
  const [showHistory, setShowHistory] = useState(false)
  
  const [showDiscovery, setShowDiscovery] = useState(false)

  const activeUser = users.find(u => u.user_id === selectedUserId)

  // Fetch active user
  useEffect(() => {
    const savedUserId = localStorage.getItem('blinkit_active_user')
    if (savedUserId) {
      setSelectedUserId(savedUserId)
      fetch(`${API_BASE}/users`)
        .then(res => res.json())
        .then(data => {
          setUsers(data)
        })
    } else {
      router.push('/')
    }
  }, [router])

  // Fetch cart
  useEffect(() => {
    if (!selectedUserId) return
    fetch(`${API_BASE}/cart/${selectedUserId}`)
      .then(res => {
        if (!res.ok) throw new Error("No cart found")
        return res.json()
      })
      .then(data => setCart(data))
      .catch(err => setCart(null))
      
    fetch(`${API_BASE}/users/${selectedUserId}/purchases`)
      .then(res => res.json())
      .then(data => setPurchases(data))
      .catch(err => setPurchases([]))
  }, [selectedUserId])

  const handleCheckout = () => {
    setShowDiscovery(true)
  }

  const completeCheckout = (acceptedRecommendation: boolean = false) => {
    setShowDiscovery(false)
    router.push(`/success?addedRec=${acceptedRecommendation}`)
  }

  const handleClearCart = async () => {
    if (!selectedUserId) return;
    if (confirm('Are you sure you want to clear your cart?')) {
      try {
        await fetch(`${API_BASE}/cart/${selectedUserId}/clear`, {
          method: 'DELETE',
        });
        setCart(null);
      } catch (err) {
        console.error("Failed to clear cart", err);
      }
    }
  }

  const handleRemoveItem = async (productId: string) => {
    if (!selectedUserId) return;
    try {
      await fetch(`${API_BASE}/cart/${selectedUserId}/item/${productId}`, {
        method: 'DELETE',
      });
      
      // Refresh cart
      const res = await fetch(`${API_BASE}/cart/${selectedUserId}`);
      if (res.ok) {
        setCart(await res.json());
      } else {
        setCart(null);
      }
    } catch (err) {
      console.error("Failed to remove item", err);
    }
  }

  return (
    <div className="bg-gray-50 min-h-screen pb-32">
      <div className="bg-white p-4 shadow-sm flex items-center justify-between sticky top-0 z-40">
        <div className="flex items-center">
          <button onClick={() => router.push('/')} className="mr-3 bg-gray-50 p-1.5 rounded-full hover:bg-gray-100 transition-colors">
            <ArrowLeft size={20} className="text-gray-700" />
          </button>
          <h1 className="text-lg font-extrabold text-gray-800 tracking-tight">Checkout</h1>
        </div>
        
        {cart && cart.items && cart.items.length > 0 && (
          <button 
            onClick={handleClearCart} 
            className="flex items-center text-xs font-bold text-red-500 hover:text-red-700 transition-colors bg-red-50 px-2.5 py-1.5 rounded-lg"
          >
            <Trash2 size={14} className="mr-1" /> Clear
          </button>
        )}
      </div>

      <div className="p-4">
        {!cart || cart.items.length === 0 ? (
          <div className="bg-white rounded-xl shadow-sm p-8 text-center border border-gray-100">
            <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-3">
              <ShoppingBag size={24} className="text-gray-400" />
            </div>
            <h3 className="font-bold text-gray-800 mb-1">Your cart is empty</h3>
            <p className="text-sm text-gray-500 mb-4">Add items from the homepage to proceed.</p>
            <button 
              onClick={() => router.push('/')}
              className="bg-green-600 text-white font-bold py-2 px-6 rounded-lg text-sm"
            >
              Start Shopping
            </button>
          </div>
        ) : (
          <>
            <div className="bg-white rounded-xl shadow-sm p-4 mb-4">
          <h2 className="font-bold text-gray-800 mb-4 flex items-center">
            <ShoppingBag size={18} className="mr-2 text-gray-500" /> Items
          </h2>
          
          {cart && cart.items && cart.items.length > 0 ? cart.items.map((item: any, idx: number) => (
            <div key={idx} className="flex items-center justify-between border-b pb-3 mb-3 last:border-0 last:pb-0 last:mb-0">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-gray-100 rounded-lg mr-3 flex items-center justify-center overflow-hidden">
                  <img src={item.image_url} alt={item.name} className="w-full h-full object-cover" />
                </div>
                <div>
                  <div className="text-sm font-semibold text-gray-800">{item.name}</div>
                  <div className="text-xs text-gray-500">{item.quantity} unit(s)</div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="font-bold text-sm">₹{item.selling_price * item.quantity}</div>
                <button 
                  onClick={() => handleRemoveItem(item.product_id || item.id)}
                  className="text-gray-400 hover:text-red-500 transition-colors p-1"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          )) : (
            <div className="text-sm text-gray-500 text-center py-4">No items in cart for this user.</div>
              )}
            </div>

            {/* Checkout Enhancements */}
            <div className="bg-white rounded-xl shadow-sm p-4 mb-4">
              <div className="flex items-start justify-between mb-3 border-b border-gray-100 pb-3">
                <div className="flex items-start">
                  <div className="bg-gray-50 p-2 rounded-lg mr-3">
                    <MapPin size={18} className="text-gray-600" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-gray-800">Delivery Address</h3>
                    <p className="text-xs text-gray-500 mt-0.5">Home, 123 Main Street, Appt 4B</p>
                  </div>
                </div>
                <button className="text-xs font-bold text-green-600">Change</button>
              </div>
              <div className="flex items-center">
                <div className="bg-green-50 p-2 rounded-lg mr-3">
                  <Clock size={18} className="text-green-600" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-gray-800">Delivery in 10 minutes</h3>
                  <p className="text-xs text-gray-500 mt-0.5">Shipment from nearest dark store</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-4 mb-4">
              <h2 className="font-bold text-gray-800 mb-3 flex items-center">
                <Receipt size={18} className="mr-2 text-gray-500" /> Bill Details
              </h2>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between text-gray-600">
                  <span>Item Total</span>
                  <span>₹{cart.cart_value}</span>
                </div>
                <div className="flex justify-between text-gray-600">
                  <span>Delivery Fee</span>
                  <span>₹15</span>
                </div>
                <div className="flex justify-between text-gray-600">
                  <span>Handling Fee</span>
                  <span>₹2</span>
                </div>
                <div className="flex justify-between font-bold text-gray-800 pt-2 border-t border-gray-100">
                  <span>Grand Total</span>
                  <span>₹{cart.cart_value + 17}</span>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-4 mb-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className="bg-blue-50 p-2 rounded-lg mr-3">
                    <CreditCard size={18} className="text-blue-600" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-gray-800">Pay via UPI</h3>
                    <p className="text-xs text-gray-500 mt-0.5">Google Pay, PhonePe, Paytm</p>
                  </div>
                </div>
                <button className="text-xs font-bold text-green-600">Change</button>
              </div>
            </div>
          </>
        )}
      </div>

      {/* Sticky Bottom Bar */}
      <div className="fixed bottom-0 w-full max-w-md bg-white border-t p-4 shadow-[0_-15px_40px_rgba(0,0,0,0.08)] z-30">
        <div className="flex items-center justify-between mb-3">
          <span className="text-sm font-semibold text-gray-600">To Pay</span>
          <span className="text-xl font-extrabold text-gray-900">₹{cart ? cart.cart_value + 17 : 0}</span>
        </div>
        <button 
          onClick={handleCheckout}
          disabled={!cart}
          className="w-full bg-green-600 text-white font-extrabold py-3.5 rounded-xl shadow-lg shadow-green-600/20 hover:bg-green-700 transition-all disabled:opacity-50 disabled:shadow-none"
        >
          Proceed to Pay
        </button>
      </div>

      {showDiscovery && (
        <SmartDiscoveryModal 
          userId={selectedUserId}
          activeUser={activeUser}
          onSkip={(payload) => completeCheckout(false)}
          onAccept={(payload) => completeCheckout(true)}
        />
      )}
    </div>
  )
}
