'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useSession, signOut } from 'next-auth/react';
import { AnimatePresence, motion } from 'framer-motion';

export default function Header() {
  const { data: session } = useSession();
  const [showMenu, setShowMenu] = useState(false);

  const userName = session?.user?.name || session?.user?.email?.split('@')[0] || 'User';

  return (
    <header className="sticky top-0 z-30 w-full glass border-b border-white/20 shadow-xl backdrop-blur-lg">
      <div className="max-w-5xl mx-auto flex items-center justify-between px-6 py-3">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2">
          <span className="text-primary font-bold text-2xl tracking-tight" style={{ fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif', letterSpacing: '-0.02em' }}>Curi</span>
        </Link>
        {/* Navigation */}
        <nav className="hidden md:flex gap-8 text-base font-medium">
          <Link href="/chat" className="hover:text-primary transition-colors">Chat</Link>
          <Link href="/preferences" className="hover:text-primary transition-colors">Preferences</Link>
          <Link href="/explore" className="hover:text-primary transition-colors">Explore</Link>
        </nav>
        {/* User menu */}
        <div className="relative">
          <button
            onClick={() => setShowMenu((v) => !v)}
            className="px-4 py-2 rounded-full glass border border-primary/30 text-primary font-semibold shadow-md hover:shadow-lg hover:border-primary/60 transition-all"
            style={{ fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif' }}
          >
            {userName}
          </button>
          <AnimatePresence>
            {showMenu && (
              <motion.div
                initial={{ opacity: 0, y: -8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ duration: 0.18 }}
                className="absolute right-0 mt-2 min-w-[160px] glass border border-white/30 shadow-xl rounded-2xl py-2 z-50"
              >
                <button
                  onClick={() => signOut({ callbackUrl: '/' })}
                  className="w-full text-left px-4 py-2 text-text font-medium rounded-xl transition-colors hover:text-error hover:bg-error/10"
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