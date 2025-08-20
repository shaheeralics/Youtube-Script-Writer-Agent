# YouTube Script Writer AI 🎬

A futuristic AI-powered YouTube script generator built with React and Tailwind CSS.

## ✨ Features

- **AI-Powered Generation**: Advanced script generation using Google's Gemini AI
- **Futuristic UI**: Clean, modern interface with cyber-themed design
- **Real-time Preview**: Instant script generation and editing
- **Export Options**: Download scripts as text files
- **Responsive Design**: Works perfectly on all devices
- **GitHub Pages Ready**: Deployed and accessible online

## 🚀 Live Demo

Visit the live application: [YouTube Script Writer AI](https://shaheeralics.github.io/Youtube-Script-Writer-Agent)

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern JavaScript library
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Beautiful icons
- **PostCSS** - CSS processing

### Backend (Coming Soon)
- **FastAPI/Flask** - Python backend for API key protection
- **Google Gemini AI** - Advanced language model
- **Deployment** - Render/Railway/Vercel

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/shaheeralics/Youtube-Script-Writer-Agent.git
   cd Youtube-Script-Writer-Agent
   ```

2. **Install dependencies**
   
   **For React Frontend:**
   ```bash
   npm install
   ```
   
   **For Python Backend:**
   ```bash
   pip install -r streamlit/requirements.txt
   ```

3. **Start the development servers**
   
   **React Frontend:**
   ```bash
   npm start
   ```
   
   **Streamlit Backend:**
   ```bash
   streamlit run app.py
   ```

4. **Build for production**
   ```bash
   npm run build
   ```

5. **Deploy to GitHub Pages**
   - **Automatic**: Push to `main` branch - GitHub Actions will deploy automatically
   - **Manual**: Go to GitHub repo → Actions tab → Run "Deploy React App to GitHub Pages"

## 🎨 Design Features

- **Cyber-themed UI** with neon accents
- **Glass morphism** cards and components
- **Animated backgrounds** with floating orbs
- **Smooth transitions** and hover effects
- **Responsive grid** layout
- **Custom scrollbars** and loading states

## 📁 Project Structure

```
Youtube-Script-Writer-Agent/
├── public/                 # Static files for React
├── src/                   # React source code
│   ├── App.js            # Main application component
│   ├── index.js          # React entry point
│   └── index.css         # Global styles with Tailwind
├── streamlit/            # Python/Streamlit backend files
│   ├── requirements.txt  # Python dependencies
│   ├── sample_scripts.docx # Reference scripts
│   ├── prompt.txt        # AI prompt template
│   └── *.py             # Additional Python files
├── assets/               # Additional assets
├── app.py               # Main Streamlit application
├── package.json         # Node.js dependencies
└── tailwind.config.js   # Tailwind configuration
```

## 🔧 Configuration

### Tailwind CSS
The project uses a custom Tailwind configuration with:
- Custom color palette (primary, dark themes)
- Extended animations (glow, float, pulse)
- Custom fonts (JetBrains Mono)
- Glass morphism utilities

### GitHub Pages
Configured for deployment with:
- Homepage URL in package.json
- Build and deploy scripts
- Static file serving

## 🚀 Deployment

The frontend is automatically deployed to GitHub Pages. The backend will be deployed separately to handle API key protection.

### Frontend Deployment
```bash
npm run deploy
```

### Backend Deployment (Coming Soon)
Will be deployed to Render/Railway/Vercel with environment variables for API keys.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powerful language processing
- Tailwind CSS for the amazing utility-first framework
- Lucide for beautiful icons
- React team for the excellent framework

---

**Built with ❤️ by [Shaheer Ali](https://github.com/shaheeralics)**
