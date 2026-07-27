import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Navbar from '@/components/Navbar'
import BottomNav from '@/components/BottomNav'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Blinkit MVP',
  description: 'AI Smart Discovery Engine',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gray-100 flex justify-center min-h-screen`}>
        {/* Simulating Mobile View */}
        <div className="w-full max-w-md bg-white shadow-2xl relative min-h-screen flex flex-col overflow-hidden">
          <Navbar />
          <main className="pt-16 flex-1 overflow-y-auto">{children}</main>
          <BottomNav />
        </div>
      </body>
    </html>
  )
}
