import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Sparkles, Brain, Lightbulb, Zap } from 'lucide-react';

interface PromptInputProps {
  onGenerate: (prompt: string) => void;
  onReset: () => void;
  isGenerating: boolean;
  disabled: boolean;
  aiStatus: 'idle' | 'connecting' | 'analyzing' | 'planning' | 'generating' | 'assembling' | 'validating' | 'complete' | 'error';
}

const PromptInput = ({
  onGenerate,
  onReset,
  isGenerating,
  disabled,
  aiStatus
}: PromptInputProps) => {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim() && !disabled) {
      onGenerate(prompt.trim());
    }
  };

  const handleReset = () => {
    setPrompt('');
    onReset();
  };

  const getButtonText = () => {
    switch (aiStatus) {
      case 'connecting': return 'Connecting to AI...';
      case 'analyzing': return 'AI Analyzing...';
      case 'planning': return 'AI Planning...';
      case 'generating': return 'AI Creating...';
      case 'assembling': return 'AI Assembling...';
      case 'validating': return 'AI Validating...';
      case 'complete': return 'Generation Complete';
      case 'error': return 'Try Again';
      default: return 'Generate with AI';
    }
  };

  const getButtonIcon = () => {
    switch (aiStatus) {
      case 'analyzing': return <Brain className="w-5 h-5 animate-pulse" />;
      case 'planning': return <Lightbulb className="w-5 h-5 animate-bounce" />;
      case 'generating': return <Zap className="w-5 h-5 animate-spin" />;
      case 'complete': return <Sparkles className="w-5 h-5" />;
      default: return <Send className="w-5 h-5" />;
    }
  };

  const examplePrompts = [
    "Create a modern portfolio website for a UX designer",
    "Build a restaurant website with menu and reservations",
    "Design a tech startup landing page with pricing",
    "Create a photography portfolio with gallery"
  ];

  return (
    <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-8">
      {/* Clean header with proper typography hierarchy */}
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-neutral-50 tracking-tight mb-2">
          Describe Your Website
        </h1>
        <p className="text-neutral-400">
          Provide a detailed description and our AI will generate a complete website for you.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Clean textarea with focus states */}
        <div className="space-y-2">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Example: Create a modern portfolio website for a freelance graphic designer. Include a hero section, about page, portfolio gallery, services overview, and contact form. Use a clean, minimal design with a blue and white color scheme."
            className="w-full h-32 px-4 py-3 bg-neutral-900 border border-neutral-800 rounded-lg text-lg text-neutral-100 placeholder-neutral-500 resize-none transition-colors duration-200 focus-ring hover:border-neutral-700 focus:border-blue-500"
            disabled={disabled}
            maxLength={3000}
          />
          
          {/* Clean character counter */}
          <div className="flex justify-between items-center text-sm">
            <span className="text-neutral-500">
              Be specific for best results
            </span>
            <span className={`font-mono ${
              prompt.length > 2700 ? 'text-orange-400' : 
              prompt.length > 2900 ? 'text-red-400' : 'text-neutral-500'
            }`}>
              {prompt.length}/3000
            </span>
          </div>
        </div>

        {/* Example prompts with clean styling */}
        <div className="space-y-3">
          <label className="text-sm font-medium text-neutral-400">
            Quick Start Examples
          </label>
          <div className="flex flex-wrap gap-2">
            {examplePrompts.map((example, index) => (
              <button
                key={index}
                type="button"
                onClick={() => !disabled && setPrompt(example)}
                className="text-sm px-3 py-2 bg-neutral-800 hover:bg-neutral-700 text-neutral-300 hover:text-neutral-100 rounded-md transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed border border-neutral-700 hover:border-neutral-600"
                disabled={disabled}
              >
                {example}
              </button>
            ))}
          </div>
        </div>

        {/* Action buttons with proper hierarchy */}
        <div className="flex gap-4">
          <button
            type="submit"
            disabled={!prompt.trim() || disabled}
            className="flex-1 flex items-center justify-center gap-3 px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-neutral-600 text-white font-semibold rounded-lg transition-all duration-200 disabled:cursor-not-allowed hover-scale shadow-glow disabled:shadow-none focus-ring"
          >
            {isGenerating ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>Generating...</span>
              </>
            ) : (
              <>
                <span>{getButtonText()}</span>
                {getButtonIcon()}
              </>
            )}
          </button>

          <button
            type="button"
            onClick={handleReset}
            disabled={disabled && !isGenerating}
            className="px-4 py-3 bg-neutral-700 hover:bg-neutral-600 text-neutral-300 hover:text-neutral-100 rounded-lg transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed focus-ring"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
        </div>
      </form>

      {/* AI Tips */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="p-4 bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-xl"
      >
        <div className="flex items-start gap-3">
          <Brain className="w-5 h-5 text-blue-600 mt-0.5" />
          <div>
            <h4 className="font-medium text-blue-800 mb-1">AI Tips for Better Results</h4>
            <ul className="text-sm text-blue-700 space-y-1">
              <li>• Be specific about the type of website (portfolio, business, blog)</li>
              <li>• Mention your target audience and purpose</li>
              <li>• Include style preferences (modern, minimal, colorful)</li>
              <li>• Specify key features you need (contact forms, galleries, etc.)</li>
            </ul>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default PromptInput;