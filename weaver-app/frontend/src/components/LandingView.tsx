import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Zap, Code2, Palette } from 'lucide-react';
import { useAppStore } from '../store/appStore';

export const LandingView: React.FC = () => {
  const hideLandingView = useAppStore((state) => state.hideLandingView);

  const handleGetStarted = () => {
    hideLandingView();
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.8, ease: [0.4, 0, 0.2, 1] }}
      className="fixed inset-0 z-50 flex items-center justify-center min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100"
    >
      {/* Animated Background Orbs */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          animate={{
            x: [0, 100, 0],
            y: [0, -100, 0],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: "linear"
          }}
          className="absolute top-1/4 left-1/4 w-64 h-64 bg-gradient-to-r from-cyan-400/30 to-blue-500/30 rounded-full blur-3xl"
        />
        <motion.div
          animate={{
            x: [0, -50, 0],
            y: [0, 100, 0],
          }}
          transition={{
            duration: 15,
            repeat: Infinity,
            ease: "linear"
          }}
          className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-gradient-to-r from-purple-400/20 to-pink-500/20 rounded-full blur-3xl"
        />
      </div>

      {/* Main Content */}
      <div className="relative z-10 text-center max-w-4xl mx-auto px-6">
        {/* Logo/Brand */}
        <motion.div
          initial={{ y: -30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.6 }}
          className="mb-8"
        >
          <div className="inline-flex items-center gap-3 px-6 py-3 bg-white/70 backdrop-blur-xl rounded-full border border-white/20 shadow-lg">
            <div className="w-8 h-8 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-full flex items-center justify-center">
              <Code2 className="w-4 h-4 text-white" />
            </div>
            <span className="text-xl font-semibold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
              Weaver
            </span>
          </div>
        </motion.div>

        {/* Main Headline */}
        <motion.h1
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.6 }}
          className="text-6xl md:text-7xl font-bold text-shimmer mb-6 leading-tight"
        >
          AI-Powered Frontend,
          <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-600 via-purple-600 to-blue-600">
            Instantly Realized
          </span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.6, duration: 0.6 }}
          className="text-xl md:text-2xl text-gray-600 mb-12 max-w-2xl mx-auto leading-relaxed"
        >
          Transform your ideas into stunning, responsive websites with the power of AI.
          <br />
          <span className="font-medium text-gray-800">What masterpiece will we create today?</span>
        </motion.p>

        {/* Feature Pills */}
        <motion.div
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.8, duration: 0.6 }}
          className="flex flex-wrap justify-center gap-4 mb-12"
        >
          {[
            { icon: Zap, text: "Lightning Fast", color: "from-yellow-400 to-orange-500" },
            { icon: Palette, text: "Beautiful Design", color: "from-pink-400 to-rose-500" },
            { icon: Code2, text: "Clean Code", color: "from-blue-400 to-indigo-500" },
            { icon: Sparkles, text: "AI Powered", color: "from-purple-400 to-violet-500" }
          ].map((feature, index) => (
            <motion.div
              key={feature.text}
              initial={{ scale: 0, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.8 + (index * 0.1), duration: 0.4 }}
              className="flex items-center gap-2 px-4 py-2 bg-white/60 backdrop-blur-xl rounded-full border border-white/30 shadow-sm"
            >
              <div className={`w-6 h-6 rounded-full bg-gradient-to-r ${feature.color} flex items-center justify-center`}>
                <feature.icon className="w-3 h-3 text-white" />
              </div>
              <span className="text-sm font-medium text-gray-700">{feature.text}</span>
            </motion.div>
          ))}
        </motion.div>

        {/* CTA Button */}
        <motion.div
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 1.0, duration: 0.6 }}
        >
          <motion.button
            onClick={handleGetStarted}
            className="group relative px-12 py-4 bg-gradient-to-r from-cyan-500 via-purple-500 to-blue-600 text-white font-semibold text-lg rounded-full shadow-xl hover:shadow-2xl transition-all duration-300 aurora-gradient btn-kinetic focus-aurora"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <span className="relative z-10 flex items-center gap-3">
              Start Creating
              <motion.div
                animate={{ rotate: [0, 360] }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
              >
                <Sparkles className="w-5 h-5" />
              </motion.div>
            </span>
            
            {/* Button Glow Effect */}
            <div className="absolute inset-0 rounded-full bg-gradient-to-r from-cyan-500 via-purple-500 to-blue-600 blur-xl opacity-50 group-hover:opacity-75 transition-opacity duration-300" />
          </motion.button>
        </motion.div>

        {/* Subtle Call to Action */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2, duration: 0.6 }}
          className="mt-8 text-sm text-gray-500"
        >
          No sign-up required • Generate unlimited websites • Export clean code
        </motion.p>
      </div>
    </motion.div>
  );
};