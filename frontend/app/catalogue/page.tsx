import Link from 'next/link'
import { Package, ArrowLeft } from 'lucide-react'

export default function CataloguePage() {
  return (
    <div className="min-h-screen bg-gray-50 p-4 pt-20 flex flex-col items-center">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-sm border border-gray-200 p-8 space-y-6">
        
        <div className="flex flex-col items-center text-center space-y-3">
          <div className="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mb-2">
            <Package size={32} className="text-blue-500" />
          </div>
          <h1 className="text-2xl font-extrabold text-gray-900 tracking-tight">Product Catalogue</h1>
        </div>

        <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4 text-sm text-yellow-900 font-medium leading-relaxed">
          This feature is intentionally out of scope for this MVP.
        </div>

        <div className="space-y-4 text-sm text-gray-600 leading-relaxed">
          <p>
            The primary objective of this prototype is to validate Blinkit&apos;s AI-powered Smart Discovery recommendation experience during checkout and its ability to encourage cross-category product discovery.
          </p>
          
          <p>To keep the MVP focused, the following features were intentionally excluded:</p>
          
          <ul className="list-disc pl-5 space-y-1.5 font-medium text-gray-700">
            <li>Complete product catalogue</li>
            <li>Advanced search</li>
            <li>Product filters and sorting</li>
            <li>Category listing pages</li>
          </ul>
          
          <p className="italic text-gray-500">
            These features would be included in a future production-ready version.
          </p>
        </div>

        <div className="pt-4 border-t border-gray-100">
          <Link 
            href="/"
            className="w-full flex items-center justify-center bg-gray-100 hover:bg-gray-200 text-gray-800 font-extrabold py-3.5 rounded-xl transition-colors shadow-sm"
          >
            <ArrowLeft size={18} className="mr-2" />
            Back to Home
          </Link>
        </div>
        
      </div>
    </div>
  )
}
