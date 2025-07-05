import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAppStore } from './store/appStore';
import { useAIGeneration } from './hooks/useAIGeneration';
import { generateWebsite } from './utils/api';

import { LandingView } from './components/LandingView';
import { Header } from './components/Header';
import PromptInput from './components/PromptInput';
import { StatusLog } from './components/StatusLog';
import PreviewWindow from './components/PreviewWindow';
import DownloadButton from './components/DownloadButton';

import './App.css';

function App() {
  const { showLandingView, isDarkMode } = useAppStore();
  const [currentTaskId, setCurrentTaskId] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  
  // Use the Ollama generation hook with multi-step tracking
  const ollamaState = useAIGeneration(currentTaskId);

  const handleGenerate = async (prompt: string) => {
    try {
      setIsGenerating(true);
      
      // Call the Ollama-powered generation endpoint
      const response = await generateWebsite({ prompt });
      setCurrentTaskId(response.task_id);
      
      console.log('Ollama Generation started:', response.message);
    } catch (error) {
      console.error('Failed to start Ollama generation:', error);
      setIsGenerating(false);
    }
  };

  const handleReset = () => {
    setCurrentTaskId(null);
    setIsGenerating(false);
  };

  // Reset generating state when Ollama completes or errors
  React.useEffect(() => {
    if (ollamaState.status === 'complete' || ollamaState.status === 'error') {
      setIsGenerating(false);
    }
  }, [ollamaState.status]);

  if (showLandingView) {
    return (
      <AnimatePresence>
        <LandingView />
      </AnimatePresence>
    );
  }

  return (
    <div className={`min-h-screen transition-all duration-300 ${isDarkMode ? 'dark' : ''}`}>
      <Header />
      
      {/* Main Workbench */}
      <main className="pt-20 min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
        <div className="max-w-7xl mx-auto p-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-[calc(100vh-8rem)]"
          >
            {/* Left Panel - Input & Status */}
            <div className="space-y-6">
              {/* Local AI-Enhanced Prompt Input */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2, duration: 0.6 }}
                className="glass-panel rounded-2xl p-6 floating-element"
              >
                <PromptInput
                  onGenerate={handleGenerate}
                  onReset={handleReset}
                  isGenerating={isGenerating}
                  disabled={false}
                  aiStatus={ollamaState.status}
                />
              </motion.div>

              {/* Enhanced Ollama Multi-Step Status */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4, duration: 0.6 }}
                className="glass-panel rounded-2xl p-6 floating-element"
              >
                <StatusLog
                  logs={ollamaState.aiLogs}
                  currentStatus={ollamaState.currentPhase}
                  progress={ollamaState.progress}
                  aiStatus={ollamaState.status}
                  isConnected={ollamaState.isConnected}
                  currentComponent={ollamaState.currentComponent}
                  blueprintGenerated={ollamaState.blueprintGenerated}
                  componentsInProgress={ollamaState.componentsInProgress}
                  totalComponents={ollamaState.totalComponents}
                  qualityMetrics={ollamaState.qualityMetrics}
                  styleGuideGenerated={ollamaState.styleGuideGenerated}
                  currentStage={ollamaState.currentStage}
                />
              </motion.div>
            </div>

            {/* Right Panel - Preview & Download */}
            <div className="space-y-6">
              {/* Website Preview */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.6, duration: 0.6 }}
                className="glass-panel rounded-2xl p-6 floating-element flex-1"
              >
                <PreviewWindow
                  previewUrl={ollamaState.previewUrl || null}
                  isGenerating={ollamaState.isGenerating}
                />
              </motion.div>

              {/* Download Section - Only show when Ollama generation is complete */}
              {ollamaState.canDownload && ollamaState.downloadUrl && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.8, duration: 0.6 }}
                  className="glass-panel rounded-2xl p-6 floating-element"
                >
                  <DownloadButton
                    taskId={currentTaskId || ''}
                    isRealAI={false} // Ollama is local AI, not cloud AI
                  />
                </motion.div>
              )}
            </div>
          </motion.div>
        </div>
      </main>
    </div>
  );
}

export default App;
