import { useState, useEffect, useRef, useCallback } from 'react';

interface CognitiveGenerationState {
  status: 'idle' | 'connecting' | 'style_analysis' | 'blueprint_creation' | 'component_generation' | 'quality_review' | 'refinement' | 'advanced_styling' | 'final_assembly' | 'complete' | 'error';
  progress: number;
  currentPhase: string;
  currentComponent?: string;
  currentStage?: 'generating' | 'critiquing' | 'refining';
  aiLogs: string[];
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
  previewUrl?: string;
  downloadUrl?: string;
  error?: string;
  isConnected: boolean;
  isCognitiveAI: boolean;
}

export const useAIGeneration = (taskId: string | null) => {
  const [state, setState] = useState<CognitiveGenerationState>({
    status: 'idle',
    progress: 0,
    currentPhase: '',
    aiLogs: [],
    styleGuideGenerated: false,
    blueprintGenerated: false,
    componentsInProgress: [],
    totalComponents: 0,
    qualityMetrics: {
      averageScore: 0,
      totalRefinements: 0,
      critiquesCycles: 0
    },
    isConnected: false,
    isCognitiveAI: true
  });

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | undefined>(undefined);

  const connect = useCallback(() => {
    if (!taskId || wsRef.current?.readyState === WebSocket.OPEN) return;

    try {
      const ws = new WebSocket(`ws://localhost:8000/ws/generate/${taskId}`);
      wsRef.current = ws;

      ws.onopen = () => {
        setState(prev => ({ 
          ...prev, 
          isConnected: true,
          status: 'connecting',
          currentPhase: 'Connecting to Cognitive Assembly Line...'
        }));
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          
          switch (data.type) {
            case 'progress':
              setState(prev => {
                let newStatus = prev.status;
                let newStage = prev.currentStage;
                let newComponent = prev.currentComponent;
                
                // Advanced stage detection for Cognitive Assembly Line
                if (data.message.includes('Brand Strategist') || data.message.includes('aesthetic vision')) {
                  newStatus = 'style_analysis';
                } else if (data.message.includes('Architect') || data.message.includes('blueprint')) {
                  newStatus = 'blueprint_creation';
                } else if (data.message.includes('generating') && !data.message.includes('CSS')) {
                  newStatus = 'component_generation';
                  newStage = 'generating';
                  const componentMatch = data.message.match(/generating (\w+)/i);
                  if (componentMatch) {
                    newComponent = componentMatch[1];
                  }
                } else if (data.message.includes('reviewing') || data.message.includes('quality')) {
                  newStatus = 'quality_review';
                  newStage = 'critiquing';
                } else if (data.message.includes('refining')) {
                  newStatus = 'refinement';
                  newStage = 'refining';
                } else if (data.message.includes('CSS') || data.message.includes('styling')) {
                  newStatus = 'advanced_styling';
                } else if (data.message.includes('assembling')) {
                  newStatus = 'final_assembly';
                } else if (data.message.includes('complete')) {
                  newStatus = 'complete';
                }
                
                return {
                  ...prev,
                  status: newStatus,
                  currentPhase: data.message,
                  currentComponent: newComponent,
                  currentStage: newStage,
                  progress: data.progress,
                  isCognitiveAI: true
                };
              });
              break;

            case 'log':
              setState(prev => {
                const newLogs = [...prev.aiLogs, data.message];
                let updates: Partial<CognitiveGenerationState> = {
                  aiLogs: newLogs
                };
                
                // Extract Cognitive Assembly Line insights
                if (data.message.includes('Style Guide generated')) {
                  updates.styleGuideGenerated = true;
                }
                
                if (data.message.includes('Blueprint created')) {
                  const componentsMatch = data.message.match(/(\d+) components planned/);
                  if (componentsMatch) {
                    updates.blueprintGenerated = true;
                    updates.totalComponents = parseInt(componentsMatch[1]);
                  }
                }
                
                // Extract component quality scores
                if (data.message.includes('passed quality review')) {
                  const scoreMatch = data.message.match(/Score: (\d+)\/10/);
                  const componentMatch = data.message.match(/✅ (\w+) passed/);
                  if (scoreMatch && componentMatch) {
                    const score = parseInt(scoreMatch[1]);
                    const componentName = componentMatch[1];
                    updates.componentsInProgress = prev.componentsInProgress.map(comp =>
                      comp.name === componentName 
                        ? { ...comp, stage: 'complete', qualityScore: score }
                        : comp
                    );
                  }
                }
                
                if (data.message.includes('refined')) {
                  const scoreMatch = data.message.match(/Score: (\d+)\/10/);
                  const componentMatch = data.message.match(/🔄 (\w+) refined/);
                  if (scoreMatch && componentMatch) {
                    const score = parseInt(scoreMatch[1]);
                    const componentName = componentMatch[1];
                    updates.componentsInProgress = prev.componentsInProgress.map(comp =>
                      comp.name === componentName 
                        ? { ...comp, stage: 'complete', qualityScore: score }
                        : comp
                    );
                    updates.qualityMetrics = {
                      ...prev.qualityMetrics,
                      totalRefinements: prev.qualityMetrics.totalRefinements + 1
                    };
                  }
                }
                
                // Extract final quality metrics
                if (data.message.includes('Quality metrics:')) {
                  const refinementsMatch = data.message.match(/(\d+) refinements/);
                  const scoreMatch = data.message.match(/avg score: ([\d.]+)\/10/);
                  if (refinementsMatch && scoreMatch) {
                    updates.qualityMetrics = {
                      ...prev.qualityMetrics,
                      totalRefinements: parseInt(refinementsMatch[1]),
                      averageScore: parseFloat(scoreMatch[1])
                    };
                  }
                }
                
                return { ...prev, ...updates };
              });
              break;

            case 'completion':
              setState(prev => ({
                ...prev,
                status: 'complete',
                progress: 100,
                previewUrl: data.preview_url,
                downloadUrl: data.download_url,
                currentPhase: 'Cognitive Assembly Line complete! 🎉'
              }));
              break;

            case 'error':
              setState(prev => ({
                ...prev,
                status: 'error',
                error: data.message,
                currentPhase: 'Cognitive Assembly Line encountered an error'
              }));
              break;
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      ws.onclose = () => {
        setState(prev => ({ ...prev, isConnected: false }));
        
        // Auto-reconnect if generation is still in progress
        if (state.status !== 'complete' && state.status !== 'error' && state.status !== 'idle') {
          reconnectTimeoutRef.current = setTimeout(() => {
            connect();
          }, 2000);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setState(prev => ({
          ...prev,
          isConnected: false,
          status: 'error',
          error: 'Connection to Cognitive Assembly Line failed'
        }));
      };

    } catch (error) {
      console.error('Failed to establish WebSocket connection:', error);
      setState(prev => ({
        ...prev,
        status: 'error',
        error: 'Failed to connect to Cognitive Assembly Line'
      }));
    }
  }, [taskId, state.status]);

  useEffect(() => {
    if (taskId) {
      connect();
    }

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [taskId, connect]);

  // Reset state when taskId changes
  useEffect(() => {
    if (taskId) {
      setState({
        status: 'idle',
        progress: 0,
        currentPhase: '',
        aiLogs: [],
        styleGuideGenerated: false,
        blueprintGenerated: false,
        componentsInProgress: [],
        totalComponents: 0,
        qualityMetrics: {
          averageScore: 0,
          totalRefinements: 0,
          critiquesCycles: 0
        },
        isConnected: false,
        isCognitiveAI: true
      });
    }
  }, [taskId]);

  return {
    ...state,
    reconnect: connect,
    // Helper methods for Cognitive Assembly Line
    isGenerating: ['connecting', 'style_analysis', 'blueprint_creation', 'component_generation', 'quality_review', 'refinement', 'advanced_styling', 'final_assembly'].includes(state.status),
    canDownload: state.status === 'complete' && state.downloadUrl,
    componentProgress: state.totalComponents > 0 ? (state.componentsInProgress.filter(c => c.stage === 'complete').length / state.totalComponents) * 100 : 0,
    currentProcessingStage: state.currentStage || 'analyzing'
  };
};