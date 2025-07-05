import React from 'react';
import { motion } from 'framer-motion';
import { Code2, Moon, Sun, FileText, Sparkles } from 'lucide-react';
import { useAppStore } from '../store/appStore';

export const Header: React.FC = () => {
  const { isDarkMode, toggleDarkMode } = useAppStore();

  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: [0.4, 0, 0.2, 1] }}
      className="fixed top-0 left-0 right-0 z-40 glass-panel border-b border-white/20 backdrop-blur-xl"
    >
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="flex items-center gap-3 cursor-pointer"
          >
            <div className="w-10 h-10 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
              <Code2 className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-shimmer">Weaver</h1>
              <p className="text-xs text-gray-500 -mt-1">AI Frontend Studio</p>
            </div>
          </motion.div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center gap-6">
            {[
              { icon: Sparkles, label: 'Showcase', href: '#showcase' },
              { icon: FileText, label: 'Docs', href: '#docs' },
            ].map((item) => (
              <motion.a
                key={item.label}
                href={item.href}
                whileHover={{ y: -2 }}
                className="flex items-center gap-2 px-4 py-2 rounded-full hover:bg-white/20 transition-all duration-200 text-gray-700 hover:text-gray-900 group"
              >
                <item.icon className="w-4 h-4 group-hover:text-purple-600 transition-colors" />
                <span className="font-medium">{item.label}</span>
              </motion.a>
            ))}
          </nav>

          {/* Controls */}
          <div className="flex items-center gap-3">
            {/* Dark Mode Toggle */}
            <motion.button
              onClick={toggleDarkMode}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              className="p-3 rounded-full bg-white/20 hover:bg-white/30 transition-all duration-200 focus-aurora"
              aria-label={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              <motion.div
                animate={{ rotate: isDarkMode ? 0 : 180 }}
                transition={{ duration: 0.3 }}
              >
                {isDarkMode ? (
                  <Sun className="w-5 h-5 text-yellow-600" />
                ) : (
                  <Moon className="w-5 h-5 text-gray-700" />
                )}
              </motion.div>
            </motion.button>

            {/* Status Indicator */}
            <div className="flex items-center gap-2 px-3 py-2 bg-white/20 rounded-full">
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="w-2 h-2 bg-green-500 rounded-full shadow-sm"
              />
              <span className="text-xs font-medium text-gray-700">Ready</span>
            </div>
          </div>
        </div>
      </div>
    </motion.header>
  );
};