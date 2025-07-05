import { useState } from 'react';

interface PreviewWindowProps {
  previewUrl: string | null;
  isGenerating: boolean;
}

const PreviewWindow = ({ previewUrl, isGenerating }: PreviewWindowProps) => {
  const [selectedDevice, setSelectedDevice] = useState<'desktop' | 'tablet' | 'mobile'>('desktop');
  const [isLoading, setIsLoading] = useState(false);

  const deviceConfigs = {
    desktop: { width: '100%', height: '600px', icon: '💻' },
    tablet: { width: '768px', height: '600px', icon: '📱' },
    mobile: { width: '375px', height: '600px', icon: '📱' }
  };

  const handleDeviceChange = (device: 'desktop' | 'tablet' | 'mobile') => {
    setSelectedDevice(device);
    setIsLoading(true);
    setTimeout(() => setIsLoading(false), 300);
  };

  return (
    <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-6">
      {/* Clean header with device controls */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-neutral-50 tracking-tight">
          Website Preview
        </h2>
        
        {previewUrl && (
          <div className="flex items-center gap-1 bg-neutral-800 rounded-lg p-1">
            {Object.entries(deviceConfigs).map(([device, config]) => (
              <button
                key={device}
                onClick={() => handleDeviceChange(device as 'desktop' | 'tablet' | 'mobile')}
                className={`flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                  selectedDevice === device
                    ? 'bg-blue-600 text-white'
                    : 'text-neutral-400 hover:text-neutral-200 hover:bg-neutral-700'
                }`}
              >
                <span>{config.icon}</span>
                <span className="capitalize">{device}</span>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Preview container */}
      <div className="bg-neutral-950 border border-neutral-800 rounded-lg p-4 min-h-[600px]">
        {!previewUrl ? (
          <div className="flex items-center justify-center h-[600px] text-neutral-500">
            <div className="text-center">
              {isGenerating ? (
                <>
                  <div className="flex items-center justify-center mb-4">
                    <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
                  </div>
                  <h3 className="text-lg font-medium text-neutral-400 mb-2">
                    Generating Website
                  </h3>
                  <p className="text-neutral-500">
                    Your website preview will appear here once generation is complete
                  </p>
                </>
              ) : (
                <>
                  <div className="text-4xl mb-4">🌐</div>
                  <h3 className="text-lg font-medium text-neutral-400 mb-2">
                    Preview Ready
                  </h3>
                  <p className="text-neutral-500">
                    Enter a website description above to generate and preview your site
                  </p>
                </>
              )}
            </div>
          </div>
        ) : (
          <div className="flex justify-center">
            <div 
              className="bg-white rounded-lg shadow-lg border border-neutral-700 overflow-hidden transition-all duration-300"
              style={{ 
                width: deviceConfigs[selectedDevice].width,
                height: deviceConfigs[selectedDevice].height,
                maxWidth: '100%'
              }}
            >
              {isLoading ? (
                <div className="flex items-center justify-center h-full bg-neutral-100">
                  <div className="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
                </div>
              ) : (
                <iframe
                  src={previewUrl}
                  className="w-full h-full border-0"
                  title="Website Preview"
                  sandbox="allow-scripts allow-same-origin allow-forms"
                />
              )}
            </div>
          </div>
        )}
      </div>

      {/* Preview controls footer */}
      {previewUrl && (
        <div className="mt-4 pt-4 border-t border-neutral-800">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <span className="text-sm text-neutral-400">
                Viewing: {selectedDevice} ({deviceConfigs[selectedDevice].width})
              </span>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 bg-green-400 rounded-full" />
                <span className="text-xs text-neutral-500">Live Preview</span>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <button
                onClick={() => window.open(previewUrl, '_blank')}
                className="flex items-center gap-2 px-3 py-1.5 text-sm bg-neutral-800 hover:bg-neutral-700 text-neutral-300 hover:text-neutral-100 rounded-md transition-colors duration-200 focus-ring"
              >
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
                <span>Open in New Tab</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PreviewWindow;