'use client'

import { usePathname } from 'next/navigation'
import Link from 'next/link'

import { useState } from 'react'
import { Info } from 'lucide-react'

export default function BottomNav() {
  const pathname = usePathname()
  const [showSearchToast, setShowSearchToast] = useState(false)
  const [showCartToast, setShowCartToast] = useState(false)

  // Hide the global bottom nav on the cart and success pages so it doesn't overlap the checkout bar
  if (pathname === '/cart' || pathname === '/success') {
    return null
  }

  const handleNotImplemented = (setToast: (val: boolean) => void) => {
    setToast(true)
    setTimeout(() => setToast(false), 4000)
  }

  return (
    <>
      <div className="absolute bottom-0 w-full bg-white/90 backdrop-blur-md border-t border-gray-100 flex justify-around p-3 z-40 pb-5 shadow-[0_-5px_20px_rgba(0,0,0,0.05)]">
      <Link href="/" className={`flex flex-col items-center transition ${pathname === '/' ? 'text-green-600' : 'text-gray-400 hover:text-gray-600'}`}>
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={pathname === '/' ? "2.5" : "2"} strokeLinecap="round" strokeLinejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
        <span className={`text-[10px] mt-1 ${pathname === '/' ? 'font-bold' : 'font-medium'}`}>Home</span>
      </Link>
      <button 
        onClick={() => handleNotImplemented(setShowSearchToast)}
        className="flex flex-col items-center text-gray-400 cursor-not-allowed transition hover:text-gray-600 focus:outline-none"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        <span className="text-[10px] mt-1 font-medium">Search</span>
      </button>
      <button 
        onClick={() => handleNotImplemented(setShowCartToast)}
        className={`flex flex-col items-center transition ${pathname === '/cart' ? 'text-green-600' : 'text-gray-400 hover:text-gray-600 focus:outline-none'}`}
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={pathname === '/cart' ? "2.5" : "2"} strokeLinecap="round" strokeLinejoin="round"><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/></svg>
        <span className={`text-[10px] mt-1 ${pathname === '/cart' ? 'font-bold' : 'font-medium'}`}>Cart</span>
      </button>

      </div>

      {showSearchToast && (
        <div className="fixed bottom-24 left-1/2 transform -translate-x-1/2 w-11/12 max-w-sm bg-gray-900 text-white text-xs p-3 rounded-lg shadow-xl z-50 animate-fade-in-up">
          <div className="flex items-start">
            <Info size={16} className="text-blue-400 mr-2 flex-shrink-0 mt-0.5" />
            <p>
              Search is not implemented in this MVP. This prototype focuses on AI-powered Smart Discovery and personalized cross-category recommendations.
            </p>
          </div>
        </div>
      )}

    {showCartToast && (
        <div className="fixed bottom-24 left-1/2 transform -translate-x-1/2 w-11/12 max-w-sm bg-gray-900 text-white text-xs p-3 rounded-lg shadow-xl z-50 animate-fade-in-up">
          <div className="flex items-start">
            <Info size={16} className="text-blue-400 mr-2 flex-shrink-0 mt-0.5" />
            <p>
              This option is not implemented in this MVP. This prototype focuses on AI-powered Smart Discovery and personalized cross-category recommendations.
            </p>
          </div>
        </div>
      )}
    </>
  )
}
