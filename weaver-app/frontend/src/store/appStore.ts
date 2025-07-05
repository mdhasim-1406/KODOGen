import { create } from 'zustand';

interface AppState {
  // Progressive Disclosure States
  showLandingView: boolean;
  showExamplePrompts: boolean;
  showAdvancedControls: boolean;
  
  // UI Theme State
  isDarkMode: boolean;
  
  // Component Visibility
  isActivityFeedExpanded: boolean;
  previewDeviceType: 'mobile' | 'tablet' | 'desktop';
}

interface AppActions {
  // Progressive Disclosure Actions
  hideLandingView: () => void;
  toggleExamplePrompts: () => void;
  toggleAdvancedControls: () => void;
  
  // Theme Actions
  toggleDarkMode: () => void;
  
  // UI Actions
  toggleActivityFeed: () => void;
  setPreviewDevice: (device: 'mobile' | 'tablet' | 'desktop') => void;
}

const initialState: AppState = {
  // Initial States - Landing view shown first for "Progressive Disclosure"
  showLandingView: true,
  showExamplePrompts: false,
  showAdvancedControls: false,
  
  // Light theme by default for "Luminous Workbench"
  isDarkMode: false,
  
  // Component states
  isActivityFeedExpanded: true,
  previewDeviceType: 'desktop',
};

export const useAppStore = create<AppState & AppActions>((set) => ({
  ...initialState,
  
  // Progressive Disclosure Actions
  hideLandingView: () => set({ showLandingView: false }),
  
  toggleExamplePrompts: () => set((state) => ({ 
    showExamplePrompts: !state.showExamplePrompts 
  })),
  
  toggleAdvancedControls: () => set((state) => ({ 
    showAdvancedControls: !state.showAdvancedControls 
  })),
  
  // Theme Actions
  toggleDarkMode: () => set((state) => ({ 
    isDarkMode: !state.isDarkMode 
  })),
  
  // UI Actions
  toggleActivityFeed: () => set((state) => ({ 
    isActivityFeedExpanded: !state.isActivityFeedExpanded 
  })),
  
  setPreviewDevice: (device) => set({ 
    previewDeviceType: device 
  }),
}));