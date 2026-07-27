'use client'
import { Search, MapPin, User, ChevronDown, Info } from 'lucide-react'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function Navbar() {
  const [activePersona, setActivePersona] = useState<any>(null)
  const [showSearchToast, setShowSearchToast] = useState(false)
  const router = useRouter()

  useEffect(() => {
    const fetchActivePersona = async () => {
      const savedUserId = localStorage.getItem('blinkit_active_user');
      if (savedUserId) {
        try {
          const res = await fetch('http://localhost:8000/api/users');
          const users = await res.json();
          const user = users.find((u: any) => u.user_id === savedUserId);
          if (user) {
            setActivePersona(user);
          }
        } catch (err) {
          console.error(err);
        }
      }
    };

    fetchActivePersona();
    
    const handlePersonaChange = () => fetchActivePersona();
    window.addEventListener('personaChanged', handlePersonaChange);
    return () => window.removeEventListener('personaChanged', handlePersonaChange);
  }, []);

  return (
    <header className="absolute top-0 w-full bg-white shadow-sm z-40">
      <div className="flex items-center justify-between px-4 py-3">
        <div className="flex flex-col">
          <div className="text-sm font-extrabold flex items-center tracking-tight text-gray-800">
            Delivery in 10 minutes
          </div>
          <div className="text-xs text-gray-500 flex items-center mt-0.5 font-medium">
            <MapPin size={12} className="mr-1 text-green-600 fill-current" />
            B-45, Sector 4, Noida <ChevronDown size={14} className="ml-1" />
          </div>
        </div>
        {activePersona ? (
          <div className="flex flex-col items-end">
            <div className="flex items-center bg-green-50 border border-green-100 px-2 py-1 rounded-full shadow-sm">
              <span className="text-xs text-green-700 font-bold flex items-center gap-1">
                <span className="text-base leading-none">👤</span> {activePersona.name}
              </span>
            </div>
            <button 
              onClick={() => router.push('/')} 
              className="text-[10px] text-gray-500 underline mt-1 hover:text-green-600 transition-colors"
            >
              Change Persona
            </button>
          </div>
        ) : (
          <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-gray-600">
            <User size={18} />
          </div>
        )}
      </div>
      <div className="px-4 pb-3">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search size={16} className="text-gray-400" />
          </div>
          <input 
            type="text" 
            readOnly
            onClick={() => {
              setShowSearchToast(true)
              setTimeout(() => setShowSearchToast(false), 4000)
            }}
            className="block w-full pl-10 pr-3 py-2.5 border border-gray-200 rounded-xl leading-5 bg-gray-50 placeholder-gray-500 focus:outline-none cursor-pointer sm:text-sm transition-all shadow-inner" 
            placeholder="Search groceries & essentials" 
          />
        </div>
      </div>
      
      {showSearchToast && (
        <div className="fixed top-24 left-1/2 transform -translate-x-1/2 w-11/12 max-w-sm bg-gray-900 text-white text-xs p-3 rounded-lg shadow-xl z-50 animate-fade-in-up">
          <div className="flex items-start">
            <Info size={16} className="text-blue-400 mr-2 flex-shrink-0 mt-0.5" />
            <p>
              Search is not implemented in this MVP. This prototype focuses on AI-powered Smart Discovery and personalized cross-category recommendations.
            </p>
          </div>
        </div>
      )}
    </header>
  )
}
