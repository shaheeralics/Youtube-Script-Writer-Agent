<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Script Writer AI - TechFela</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: #e2e8f0;
            line-height: 1.6;
            overflow-x: hidden;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        .hero {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(147, 51, 234, 0.1));
            border: 1px solid rgba(59, 130, 246, 0.2);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 60px 40px;
            margin: 40px 0;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .hero::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(from 0deg, transparent, rgba(59, 130, 246, 0.1), transparent);
            animation: rotate 8s linear infinite;
            z-index: -1;
        }
        
        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        .hero h1 {
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 20px;
            text-shadow: 0 0 30px rgba(59, 130, 246, 0.5);
        }
        
        .hero p {
            font-size: 1.3rem;
            margin-bottom: 30px;
            color: #cbd5e1;
        }
        
        .apps-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin: 40px 0;
        }
        
        .app-card {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(147, 51, 234, 0.05));
            border: 1px solid rgba(59, 130, 246, 0.3);
            backdrop-filter: blur(15px);
            border-radius: 16px;
            padding: 30px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .app-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
            transition: left 0.5s ease;
        }
        
        .app-card:hover::before {
            left: 100%;
        }
        
        .app-card:hover {
            transform: translateY(-10px);
            border-color: rgba(59, 130, 246, 0.6);
            box-shadow: 0 20px 40px rgba(59, 130, 246, 0.2);
        }
        
        .app-icon {
            width: 60px;
            height: 60px;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }
        
        .app-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #f8fafc;
            margin-bottom: 10px;
        }
        
        .app-desc {
            color: #cbd5e1;
            margin-bottom: 20px;
        }
        
        .btn {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            text-decoration: none;
            display: inline-block;
            font-weight: 600;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s ease;
        }
        
        .btn:hover::before {
            left: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3);
        }
        
        .features {
            background: linear-gradient(135deg, rgba(147, 51, 234, 0.1), rgba(236, 72, 153, 0.05));
            border: 1px solid rgba(147, 51, 234, 0.2);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 40px;
            margin: 40px 0;
        }
        
        .features h2 {
            font-size: 2.5rem;
            color: #f8fafc;
            margin-bottom: 30px;
            text-align: center;
            background: linear-gradient(135deg, #8b5cf6, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        
        .feature-item {
            background: rgba(59, 130, 246, 0.05);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s ease;
        }
        
        .feature-item:hover {
            background: rgba(59, 130, 246, 0.1);
            border-color: rgba(59, 130, 246, 0.4);
        }
        
        .feature-icon {
            font-size: 2rem;
            margin-bottom: 10px;
        }
        
        .feature-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #f8fafc;
            margin-bottom: 8px;
        }
        
        .tech-stack {
            background: linear-gradient(135deg, rgba(236, 72, 153, 0.1), rgba(59, 130, 246, 0.05));
            border: 1px solid rgba(236, 72, 153, 0.2);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 40px;
            margin: 40px 0;
        }
        
        .tech-stack h2 {
            font-size: 2.5rem;
            color: #f8fafc;
            margin-bottom: 30px;
            text-align: center;
            background: linear-gradient(135deg, #ec4899, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .tech-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        
        .tech-item {
            background: rgba(236, 72, 153, 0.05);
            border: 1px solid rgba(236, 72, 153, 0.2);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .tech-item:hover {
            background: rgba(236, 72, 153, 0.1);
            border-color: rgba(236, 72, 153, 0.4);
            transform: translateY(-5px);
        }
        
        .footer {
            text-align: center;
            padding: 40px 0;
            color: #94a3b8;
            border-top: 1px solid rgba(59, 130, 246, 0.2);
            margin-top: 60px;
        }
        
        .footer a {
            color: #3b82f6;
            text-decoration: none;
            font-weight: 600;
        }
        
        .footer a:hover {
            color: #8b5cf6;
        }
        
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 2.5rem;
            }
            
            .hero p {
                font-size: 1.1rem;
            }
            
            .apps-grid {
                grid-template-columns: 1fr;
            }
            
            .features h2,
            .tech-stack h2 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>🚀 YouTube Script Writer AI</h1>
            <p>Next-Generation AI-Powered Script Generation Platform</p>
            <p><strong>One Repository • Two Powerful Applications • Infinite Possibilities</strong></p>
        </div>
        
        <div class="apps-grid">
            <div class="app-card">
                <div class="app-icon">⚡</div>
                <h3 class="app-title">FastAPI + React App</h3>
                <p class="app-desc">Futuristic web application with cutting-edge UI design, real-time script generation, and professional PDF export functionality.</p>
                <ul style="color: #cbd5e1; margin-bottom: 20px;">
                    <li>🎨 Glass Morphism UI with animated gradients</li>
                    <li>⚡ Real-time script generation with AI</li>
                    <li>📱 Mobile-responsive design</li>
                    <li>📄 Professional PDF download</li>
                    <li>🌟 Markdown preview with syntax highlighting</li>
                </ul>
                <a href="https://youscrip.neufera.com" class="btn" target="_blank">Launch React App</a>
            </div>
            
            <div class="app-card">
                <div class="app-icon">🔬</div>
                <h3 class="app-title">Streamlit Research App</h3>
                <p class="app-desc">Advanced research and development platform for script generation with TechFela integration and Roman Urdu prompts.</p>
                <ul style="color: #cbd5e1; margin-bottom: 20px;">
                    <li>🧪 Research & development interface</li>
                    <li>🤖 TechFela Roman Urdu integration</li>
                    <li>📊 Advanced analytics and metrics</li>
                    <li>🔧 Developer tools and debugging</li>
                    <li>📈 Performance monitoring</li>
                </ul>
                <a href="https://techfela.streamlit.app" class="btn" target="_blank">Launch Streamlit App</a>
            </div>
        </div>
        
        <div class="features">
            <h2>🌟 Revolutionary Features</h2>
            <div class="features-grid">
                <div class="feature-item">
                    <div class="feature-icon">🤖</div>
                    <div class="feature-title">AI-Powered Generation</div>
                    <p>Advanced Google Gemini AI integration for intelligent script creation</p>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">🎨</div>
                    <div class="feature-title">Futuristic UI Design</div>
                    <p>Glass morphism, animated gradients, and cyber-themed aesthetics</p>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">📱</div>
                    <div class="feature-title">Mobile Responsive</div>
                    <p>Perfect performance across all devices and screen sizes</p>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">⚡</div>
                    <div class="feature-title">Real-time Preview</div>
                    <p>Instant markdown rendering with live script preview</p>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">📄</div>
                    <div class="feature-title">PDF Export</div>
                    <p>Professional PDF generation with formatted content</p>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">🌐</div>
                    <div class="feature-title">Cloud Deployment</div>
                    <p>Railway backend with GitHub Pages frontend deployment</p>
                </div>
            </div>
        </div>
        
        <div class="tech-stack">
            <h2>⚙️ Technology Stack</h2>
            <div class="tech-grid">
                <div class="tech-item">
                    <h4 style="color: #3b82f6; margin-bottom: 10px;">Frontend</h4>
                    <p>HTML5, CSS3, JavaScript<br>Responsive Design<br>Glass Morphism UI</p>
                </div>
                <div class="tech-item">
                    <h4 style="color: #8b5cf6; margin-bottom: 10px;">Backend</h4>
                    <p>FastAPI Framework<br>Python 3.9+<br>Railway Deployment</p>
                </div>
                <div class="tech-item">
                    <h4 style="color: #ec4899; margin-bottom: 10px;">AI Integration</h4>
                    <p>Google Gemini AI<br>TechFela Prompts<br>Roman Urdu Support</p>
                </div>
                <div class="tech-item">
                    <h4 style="color: #06b6d4; margin-bottom: 10px;">Research Platform</h4>
                    <p>Streamlit Framework<br>Data Analytics<br>Development Tools</p>
                </div>
            </div>
        </div>
        
        <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(147, 51, 234, 0.1)); border: 1px solid rgba(59, 130, 246, 0.2); backdrop-filter: blur(10px); border-radius: 16px; padding: 40px; margin: 40px 0; text-align: center;">
            <h2 style="font-size: 2rem; color: #f8fafc; margin-bottom: 20px;">🚀 Get Started</h2>
            <p style="color: #cbd5e1; margin-bottom: 30px; font-size: 1.1rem;">Choose your preferred platform and start generating amazing YouTube scripts!</p>
            <div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
                <a href="https://youscrip.neufera.com" class="btn" target="_blank">🌟 Launch Main App</a>
                <a href="https://techfela.streamlit.app" class="btn" target="_blank">🔬 Research Platform</a>
                <a href="https://github.com/shaheeralics/Youtube-Script-Writer-Agent" class="btn" target="_blank">📚 View Source Code</a>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="container">
            <p>Built with ❤️ and cutting-edge technology by <a href="https://github.com/shaheeralics" target="_blank">Shaheer Ali</a></p>
            <p style="margin-top: 10px; color: #64748b;">Powered by Google Gemini AI • FastAPI • Streamlit • Railway • GitHub Pages</p>
        </div>
    </div>
</body>
</html>
