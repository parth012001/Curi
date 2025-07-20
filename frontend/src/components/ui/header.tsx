'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useSession, signOut } from 'next-auth/react';
import { AnimatePresence, motion } from 'framer-motion';
import { Sparkles, ExternalLink } from 'lucide-react';

export default function Header() {
  const { data: session } = useSession();
  const [showMenu, setShowMenu] = useState(false);

  const userName = session?.user?.name || session?.user?.email?.split('@')[0] || 'User';

  return (
    <header className="sticky top-0 z-30 w-full bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto flex items-center justify-between px-6 py-4">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2">
          <Sparkles className="w-6 h-6 text-gray-800" />
          <span className="text-gray-800 font-bold text-xl tracking-tight" style={{ fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif' }}>
            Curi
          </span>
        </Link>

        {/* Navigation */}
        <nav className="flex gap-2">
          <Link 
            href="/chat" 
            className="px-4 py-2 rounded-full bg-white text-gray-800 font-medium text-sm border border-gray-300 shadow-sm"
          >
            Chat
          </Link>
          <Link 
            href="/activity" 
            className="px-4 py-2 rounded-full bg-gray-800 text-white font-medium text-sm"
          >
            My Activity
          </Link>
          <Link 
            href="/personalize" 
            className="px-4 py-2 rounded-full bg-gray-800 text-white font-medium text-sm"
          >
            Personalize
          </Link>
          <Link 
            href="/settings" 
            className="px-4 py-2 rounded-full bg-gray-800 text-white font-medium text-sm"
          >
            Settings
          </Link>
        </nav>

        {/* User Profile */}
        <div className="relative">
          <button
            onClick={() => setShowMenu((v) => !v)}
            className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white font-semibold text-sm shadow-md hover:shadow-lg transition-all"
            style={{ fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif' }}
          >
            {userName.charAt(0).toUpperCase()}
          </button>
          <AnimatePresence>
            {showMenu && (
              <motion.div
                initial={{ opacity: 0, y: -8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ duration: 0.18 }}
                className="absolute right-0 mt-2 min-w-[160px] bg-white border border-gray-200 shadow-xl rounded-lg py-2 z-50"
              >
                <button
                  onClick={() => signOut({ callbackUrl: '/' })}
                  className="w-full text-left px-4 py-2 text-gray-700 font-medium rounded-lg transition-colors hover:text-red-600 hover:bg-red-50"
                >
                  Sign Out
                </button>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </header>
  );
} 