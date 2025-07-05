import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Brain, Code, Sparkles, CheckCircle, AlertCircle, Wifi, WifiOff, Zap, Palette, Users, Target, Wrench, Award, HelpCircle } from 'lucide-react';

interface CognitiveStatusLogProps {
  logs: string[];
  currentStatus: string;
  progress: number;
  aiStatus: 'idle' | 'connecting' | 'style_analysis' | 'blueprint_creation' | 'component_generation' | 'quality_review' | 'refinement' | 'advanced_styling' | 'final_assembly' | 'complete' | 'error';
  isConnected: boolean;
  currentComponent?: string;
  currentStage?: 'generating' | 'critiquing' | 'refining';
  styleGuideGenerated: boolean;
  blueprintGenerated: boolean;
  componentsInProgress: {
    name: string;
    stage: 'generating' | 'critiquing' | 'refining' | 'complete';
    qualityScore?: number;
  }[];
  totalComponents: number;
  qualityMetrics: {
    averageScore: number;
    totalRefinements: number;
    critiquesCycles: number;
  };
}

export const StatusLog: React.FC<CognitiveStatusLogProps> = ({
  logs,
  currentStatus,
  progress,
  aiStatus,
  isConnected,
  currentComponent,
  currentStage,
  styleGuideGenerated,
  blueprintGenerated,
  componentsInProgress,
  totalComponents,
  qualityMetrics
}) => {
  const [showTooltip, setShowTooltip] = useState(false);

  const getCognitiveStatusIcon = () => {
    switch (aiStatus) {
      case 'style_analysis':
        return <Palette className="w-5 h-5 text-purple-600 animate-pulse" />;
      case 'blueprint_creation':
        return <Target className="w-5 h-5 text-blue-600 animate-bounce" />;
      case 'component_generation':
        return <Code className="w-5 h-5 text-green-600 animate-bounce" />;
      case 'quality_review':
        return <Users className="w-5 h-5 text-orange-600 animate-pulse" />;
      case 'refinement':
        return <Wrench className="w-5 h-5 text-yellow-600 animate-spin" />;
      case 'advanced_styling':
        return <Sparkles className="w-5 h-5 text-pink-600 animate-pulse" />;
      case 'final_assembly':
        return <Award className="w-5 h-5 text-indigo-600 animate-bounce" />;
      case 'complete':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-600" />;
      default:
        return <Brain className="w-5 h-5 text-gray-600" />;
    }
  };

  const getCognitiveStatusColor = () => {
    switch (aiStatus) {
      case 'style_analysis': return 'border-purple-500 bg-purple-50';
      case 'blueprint_creation': return 'border-blue-500 bg-blue-50';
      case 'component_generation': return 'border-green-500 bg-green-50';
      case 'quality_review': return 'border-orange-500 bg-orange-50';
      case 'refinement': return 'border-yellow-500 bg-yellow-50';
      case 'advanced_styling': return 'border-pink-500 bg-pink-50';
      case 'final_assembly': return 'border-indigo-500 bg-indigo-50';
      case 'complete': return 'border-green-600 bg-green-100';
      case 'error': return 'border-red-500 bg-red-50';
      default: return 'border-gray-300 bg-gray-50';
    }
  };

  const getCognitiveStatusText = () => {
    switch (aiStatus) {
      case 'style_analysis': return 'Brand Strategist Working';
      case 'blueprint_creation': return 'AI Architect Planning';
      case 'component_generation': return 'Developer Generating';
      case 'quality_review': return 'Senior Developer Reviewing';
      case 'refinement': return 'Specialist Refining';
      case 'advanced_styling': return 'Designer Styling';
      case 'final_assembly': return 'Team Leader Assembling';
      case 'complete': return 'Cognitive Assembly Complete';
      case 'error': return 'Assembly Line Error';
      default: return 'Cognitive AI Ready';
    }
  };

  const getPhaseDescription = () => {
    switch (aiStatus) {
      case 'style_analysis': return 'Analyzing aesthetic vision and creating style guide';
      case 'blueprint_creation': return 'Architecting website structure and component plan';
      case 'component_generation': return `Building ${currentComponent || 'components'} with precision`;
      case 'quality_review': return `Expert review: ${currentComponent || 'component'} quality assessment`;
      case 'refinement': return `Improving ${currentComponent || 'component'} based on feedback`;
      case 'advanced_styling': return 'Creating premium CSS with advanced animations';
      case 'final_assembly': return 'Assembling final website with quality optimizations';
      case 'complete': return 'Premium website ready for deployment';
      default: return currentStatus;
    }
  };

  const getCurrentStageIcon = () => {
    switch (currentStage) {
      case 'generating': return <Code className="w-3 h-3 text-green-500" />;
      case 'critiquing': return <Users className="w-3 h-3 text-orange-500" />;
      case 'refining': return <Wrench className="w-3 h-3 text-yellow-500" />;
      default: return <Zap className="w-3 h-3 text-blue-500" />;
    }
  };

  return (
    <div className="space-y-4">
      {/* Cognitive Assembly Line Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
          <span className="text-shimmer">Cognitive Assembly Line</span>
          <span className="px-2 py-1 text-xs bg-gradient-to-r from-purple-500 via-blue-500 to-pink-500 text-white rounded-full">
            AI Team
          </span>
          {/* What's Happening Tooltip */}
          <div className="relative">
            <button
              onMouseEnter={() => setShowTooltip(true)}
              onMouseLeave={() => setShowTooltip(false)}
              className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
            >
              <HelpCircle className="w-4 h-4" />
            </button>
            <AnimatePresence>
              {showTooltip && (
                <motion.div
                  initial={{ opacity: 0, y: -10, scale: 0.9 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: -10, scale: 0.9 }}
                  className="absolute bottom-full left-0 mb-2 w-72 p-3 bg-gray-900 text-white text-sm rounded-lg shadow-xl z-10"
                >
                  <div className="font-semibold mb-1">What's Happening?</div>
                  <p>Our AI is now reviewing its own work to improve quality, just like a professional development team would! Each component goes through generation → expert review → refinement cycles.</p>
                  <div className="absolute top-full left-4 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900"></div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </h3>
        
        {/* Connection Indicator */}
        <div className="flex items-center gap-2">
          {isConnected ? (
            <Wifi className="w-4 h-4 text-green-600" />
          ) : (
            <WifiOff className="w-4 h-4 text-red-600" />
          )}
          <span className={`text-xs ${isConnected ? 'text-green-600' : 'text-red-600'}`}>
            {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </div>

      {/* Cognitive Assembly Status Card */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className={`p-4 rounded-xl border-2 ${getCognitiveStatusColor()} transition-all duration-300`}
      >
        <div className="flex items-center gap-3 mb-3">
          <motion.div
            animate={{ 
              rotate: ['component_generation', 'refinement'].includes(aiStatus) ? 360 : 0,
              scale: aiStatus === 'quality_review' ? [1, 1.1, 1] : 1
            }}
            transition={{ 
              rotate: { duration: 2, repeat: ['component_generation', 'refinement'].includes(aiStatus) ? Infinity : 0 },
              scale: { duration: 1, repeat: aiStatus === 'quality_review' ? Infinity : 0 }
            }}
          >
            {getCognitiveStatusIcon()}
          </motion.div>
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <h4 className="font-medium text-gray-800">{getCognitiveStatusText()}</h4>
              {currentStage && (
                <div className="flex items-center gap-1 px-2 py-1 bg-white/50 rounded-full">
                  {getCurrentStageIcon()}
                  <span className="text-xs font-medium capitalize">{currentStage}</span>
                </div>
              )}
            </div>
            <p className="text-sm text-gray-600">{getPhaseDescription()}</p>
          </div>
        </div>

        {/* Overall Progress Bar */}
        <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
          <motion.div
            className="h-2 rounded-full bg-gradient-to-r from-purple-500 via-blue-500 to-pink-500"
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.5, ease: "easeOut" }}
          />
        </div>
        
        <div className="flex justify-between text-xs text-gray-500">
          <span>Cognitive Assembly Progress</span>
          <span>{progress}%</span>
        </div>
      </motion.div>

      {/* Assembly Line Progress Stages */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-panel rounded-xl p-4"
      >
        <div className="flex items-center gap-2 mb-3">
          <Users className="w-4 h-4 text-blue-600" />
          <h4 className="font-medium text-gray-800">AI Development Team</h4>
        </div>
        
        <div className="grid grid-cols-1 gap-3">
          {[
            { stage: 'style_analysis', label: 'Brand Strategist', icon: Palette, completed: styleGuideGenerated },
            { stage: 'blueprint_creation', label: 'AI Architect', icon: Target, completed: blueprintGenerated },
            { stage: 'component_generation', label: 'Developer Team', icon: Code, completed: componentsInProgress.length > 0 },
            { stage: 'quality_review', label: 'Senior Reviewers', icon: Users, completed: qualityMetrics.critiquesCycles > 0 },
            { stage: 'advanced_styling', label: 'Design Specialist', icon: Sparkles, completed: aiStatus === 'complete' },
            { stage: 'final_assembly', label: 'Team Leader', icon: Award, completed: aiStatus === 'complete' }
          ].map((item, index) => {
            const isActive = aiStatus === item.stage;
            const isCompleted = item.completed;
            
            return (
              <motion.div
                key={item.stage}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`flex items-center gap-3 p-3 rounded-lg border transition-all ${
                  isActive 
                    ? 'bg-blue-100 border-blue-300 shadow-md' 
                    : isCompleted 
                      ? 'bg-green-50 border-green-200'
                      : 'bg-gray-50 border-gray-200'
                }`}
              >
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                  isActive 
                    ? 'bg-blue-500 text-white' 
                    : isCompleted 
                      ? 'bg-green-500 text-white'
                      : 'bg-gray-300 text-gray-600'
                }`}>
                  {isCompleted ? (
                    <CheckCircle className="w-4 h-4" />
                  ) : (
                    <item.icon className={`w-4 h-4 ${isActive ? 'animate-pulse' : ''}`} />
                  )}
                </div>
                <div className="flex-1">
                  <div className="font-medium text-gray-800">{item.label}</div>
                  <div className="text-xs text-gray-600">
                    {isActive ? 'Working...' : isCompleted ? 'Complete' : 'Waiting'}
                  </div>
                </div>
                {isActive && (
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                  >
                    <Zap className="w-3 h-3 text-blue-500" />
                  </motion.div>
                )}
              </motion.div>
            );
          })}
        </div>
      </motion.div>

      {/* Component Quality Dashboard */}
      {totalComponents > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-panel rounded-xl p-4"
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <Award className="w-4 h-4 text-gold-600" />
              <h4 className="font-medium text-gray-800">Quality Dashboard</h4>
            </div>
            {qualityMetrics.averageScore > 0 && (
              <div className="flex items-center gap-1 px-2 py-1 bg-green-100 rounded-full">
                <span className="text-xs font-bold text-green-800">
                  {qualityMetrics.averageScore.toFixed(1)}/10
                </span>
              </div>
            )}
          </div>
          
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div className="text-center">
              <div className="text-lg font-bold text-blue-600">{componentsInProgress.filter(c => c.stage === 'complete').length}</div>
              <div className="text-xs text-gray-600">Components Built</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-bold text-yellow-600">{qualityMetrics.totalRefinements}</div>
              <div className="text-xs text-gray-600">Refinements Made</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-bold text-green-600">{qualityMetrics.critiquesCycles}</div>
              <div className="text-xs text-gray-600">Reviews Completed</div>
            </div>
          </div>
          
          {/* Component Quality Grid */}
          <div className="grid grid-cols-2 gap-2">
            {componentsInProgress.map((component, index) => (
              <div
                key={index}
                className={`px-2 py-1 rounded text-xs flex items-center justify-between ${
                  component.stage === 'complete' 
                    ? 'bg-green-100 text-green-800' 
                    : component.stage === 'refining'
                      ? 'bg-yellow-100 text-yellow-800'
                      : component.stage === 'critiquing'
                        ? 'bg-orange-100 text-orange-800'
                        : 'bg-blue-100 text-blue-800'
                }`}
              >
                <span className="truncate">{component.name}</span>
                {component.qualityScore && (
                  <span className="font-bold ml-1">{component.qualityScore}/10</span>
                )}
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Cognitive AI Activity Log */}
      <div className="space-y-2">
        <h4 className="text-sm font-medium text-gray-700 flex items-center gap-2">
          <Brain className="w-4 h-4" />
          Cognitive Assembly Feed
        </h4>
        
        <div className="max-h-48 overflow-y-auto space-y-1 fade-mask">
          <AnimatePresence>
            {logs.map((log, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ duration: 0.3 }}
                className="text-sm px-3 py-2 bg-white/50 rounded-lg border border-white/20"
              >
                <span className="text-gray-700">{log}</span>
              </motion.div>
            ))}
          </AnimatePresence>
          
          {logs.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <Brain className="w-8 h-8 mx-auto mb-2 opacity-50" />
              <p className="text-sm">Waiting for Cognitive Assembly Line to start...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};