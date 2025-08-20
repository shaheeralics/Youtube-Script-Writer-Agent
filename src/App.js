import React, { useState, useRef, useEffect } from 'react';
import { 
  Sparkles, 
  Download, 
  Copy, 
  Send, 
  Loader2, 
  FileText, 
  Zap,
  Brain,
  Video,
  Github
} from 'lucide-react';

function App() {
  const [topic, setTopic] = useState('');
  const [script, setScript] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const textareaRef = useRef(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [script]);

  const handleGenerate = async () => {
    if (!topic.trim()) return;
    
    setIsLoading(true);
    // Simulate API call - replace with actual backend call later
    setTimeout(() => {
      setScript(`# ${topic}\n\n## Introduction\nWelcome to this exciting journey about ${topic}...\n\n## Main Content\nIn this video, we'll explore the fascinating world of ${topic} and discover how it can transform your understanding...\n\n## Conclusion\nThank you for watching! Don't forget to like and subscribe for more amazing content about ${topic}.`);
      setIsLoading(false);
    }, 2000);
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(script);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const handleDownload = () => {
    const element = document.createElement('a');
    const file = new Blob([script], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = `youtube-script-${topic.replace(/\s+/g, '-').toLowerCase()}.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="min-h-screen bg-zinc-900 relative overflow-hidden">
      {/* Animated background grid */}
      <div className="absolute inset-0 opacity-20"></div>
      
      {/* Floating orbs */}
      <div className="absolute top-20 left-20 w-32 h-32 bg-blue-500/20 rounded-full blur-xl animate-bounce"></div>
      <div className="absolute top-60 right-32 w-24 h-24 bg-purple-500/20 rounded-full blur-xl animate-pulse" style={{animationDelay: '1s'}}></div>
      <div className="absolute bottom-32 left-1/3 w-28 h-28 bg-pink-500/20 rounded-full blur-xl animate-ping" style={{animationDelay: '2s'}}></div>

      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-12">
          <div className="flex items-center justify-center mb-6">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full blur-lg opacity-75 animate-pulse"></div>
              <div className="relative bg-zinc-800 p-4 rounded-full">
                <Video className="w-12 h-12 text-blue-400" />
              </div>
            </div>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-4">
            <span className="gradient-text">YouTube Script</span>
            <br />
            <span className="text-white">Writer AI</span>
          </h1>
          
          <p className="text-zinc-400 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed">
            Generate compelling YouTube scripts powered by advanced AI. 
            Transform your ideas into engaging content that captivates your audience.
          </p>
          
          {/* Stats */}
          <div className="flex justify-center space-x-8 mt-8">
            <div className="text-center">
              <div className="flex items-center justify-center mb-2">
                <Brain className="w-5 h-5 text-blue-400 mr-2" />
                <span className="text-2xl font-bold text-white">AI</span>
              </div>
              <p className="text-zinc-400 text-sm">Powered</p>
            </div>
            <div className="text-center">
              <div className="flex items-center justify-center mb-2">
                <Zap className="w-5 h-5 text-yellow-400 mr-2" />
                <span className="text-2xl font-bold text-white">Fast</span>
              </div>
              <p className="text-zinc-400 text-sm">Generation</p>
            </div>
            <div className="text-center">
              <div className="flex items-center justify-center mb-2">
                <Sparkles className="w-5 h-5 text-purple-400 mr-2" />
                <span className="text-2xl font-bold text-white">Quality</span>
              </div>
              <p className="text-zinc-400 text-sm">Content</p>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <div className="max-w-4xl mx-auto">
          {/* Input Section */}
          <div className="glass-card p-8 mb-8 neon-border">
            <div className="flex items-center mb-6">
              <Sparkles className="w-6 h-6 text-blue-400 mr-3" />
              <h2 className="text-2xl font-bold text-white">Create Your Script</h2>
            </div>
            
            <div className="space-y-4">
              <div>
                <label htmlFor="topic" className="block text-zinc-400 text-sm font-medium mb-2">
                  Video Topic / Idea
                </label>
                <input
                  id="topic"
                  type="text"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="Enter your video topic (e.g., 'Machine Learning for Beginners')"
                  className="w-full px-4 py-3 bg-zinc-800/70 border border-zinc-700/50 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-300"
                  onKeyPress={(e) => e.key === 'Enter' && handleGenerate()}
                />
              </div>
              
              <button
                onClick={handleGenerate}
                disabled={!topic.trim() || isLoading}
                className="cyber-button w-full py-4 px-6 rounded-xl text-white font-semibold flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>Generating Script...</span>
                  </>
                ) : (
                  <>
                    <Send className="w-5 h-5" />
                    <span>Generate Script</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Output Section */}
          {(script || isLoading) && (
            <div className="glass-card p-8 neon-border">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center">
                  <FileText className="w-6 h-6 text-blue-400 mr-3" />
                  <h2 className="text-2xl font-bold text-white">Generated Script</h2>
                </div>
                
                {script && !isLoading && (
                  <div className="flex space-x-3">
                    <button
                      onClick={handleCopy}
                      className="flex items-center space-x-2 px-4 py-2 bg-zinc-700/50 hover:bg-zinc-700/70 border border-zinc-600/30 rounded-lg text-zinc-300 hover:text-white transition-all duration-300"
                    >
                      <Copy className="w-4 h-4" />
                      <span>{copied ? 'Copied!' : 'Copy'}</span>
                    </button>
                    
                    <button
                      onClick={handleDownload}
                      className="flex items-center space-x-2 px-4 py-2 bg-blue-500/20 hover:bg-blue-500/30 border border-blue-500/30 rounded-lg text-blue-400 hover:text-blue-300 transition-all duration-300"
                    >
                      <Download className="w-4 h-4" />
                      <span>Download</span>
                    </button>
                  </div>
                )}
              </div>
              
              {isLoading ? (
                <div className="flex items-center justify-center py-12">
                  <div className="text-center">
                    <Loader2 className="w-12 h-12 text-blue-400 animate-spin mx-auto mb-4" />
                    <p className="text-zinc-400">AI is crafting your perfect script...</p>
                  </div>
                </div>
              ) : (
                <textarea
                  ref={textareaRef}
                  value={script}
                  onChange={(e) => setScript(e.target.value)}
                  className="w-full min-h-[300px] p-4 bg-zinc-800/70 border border-zinc-700/50 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-300 resize-none scrollbar-hide"
                  placeholder="Your generated script will appear here..."
                />
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <footer className="text-center mt-16 pt-8 border-t border-zinc-700/30">
          <div className="flex items-center justify-center space-x-6 mb-4">
            <a
              href="https://github.com/shaheeralics/Youtube-Script-Writer-Agent"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-2 text-zinc-400 hover:text-blue-400 transition-colors duration-300"
            >
              <Github className="w-5 h-5" />
              <span>View on GitHub</span>
            </a>
          </div>
          <p className="text-zinc-400 text-sm">
            Built with ❤️ using React, Tailwind CSS, and AI
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
