# 🎬 TechFela YouTube Script Generator

A modern, client-side YouTube script generator powered by Google's Gemini AI. Generate engaging scripts in Roman Urdu for your Pakistan-focused tech content!

## Features ✨

- 🤖 **AI-Powered Script Generation** - Uses Google Gemini 2.0 Flash API
- 📝 **Multiple Formats** - Short (60-90s) and Long (3-6 min) videos
- 🗣️ **Roman Urdu Content** - Optimized for Pakistani tech audience
- 📄 **PDF Export** - Download scripts as professional PDFs
- 📋 **Script History** - Save and manage all your generated scripts
- 💾 **Local Storage** - All data stored locally in your browser
- 🎨 **Modern UI** - Beautiful interface with Tailwind CSS
- ⚡ **No Backend Required** - Runs entirely on GitHub Pages
- 📱 **Fully Responsive** - Works perfectly on mobile and desktop

## Getting Started

### Prerequisites

- A free Google Gemini API key from [ai.google.dev](https://ai.google.dev)
- A modern web browser

### Step 1: Get Your Google Gemini API Key

1. Visit [ai.google.dev](https://ai.google.dev)
2. Click "Get API Key"
3. Create a new free project or select an existing one
4. Generate an API key
5. Keep it secure and don't share it publicly

### Step 2: Deploy to GitHub Pages

#### Option A: Fork and Deploy (Recommended)

1. **Fork this repository**
   ```bash
   # Go to the GitHub repo and click "Fork"
   ```

2. **Enable GitHub Pages**
   - Go to your fork's Settings
   - Select "Pages" from the left menu
   - Under "Source", select "Deploy from a branch"
   - Select `main` branch and `/root` folder (or `/public` if restructured)
   - Click "Save"

3. **Access Your App**
   - Your app will be available at: `https://YOUR_USERNAME.github.io/Youtube-Script-Writer`
   - Wait 2-3 minutes for GitHub Pages to build

#### Option B: Manual Setup

1. **Clone and setup**
   ```bash
   git clone https://github.com/yourusername/Youtube-Script-Writer.git
   cd Youtube-Script-Writer
   ```

2. **Copy the public folder contents to docs folder**
   ```bash
   # If using docs folder for GitHub Pages
   cp -r public/* docs/
   ```

3. **Update repository settings**
   - Go to Settings → Pages
   - Select "Deploy from a branch"
   - Choose `main` branch and `/docs` folder
   - Click Save

### Step 3: Use the App

1. Open your GitHub Pages URL in a browser
2. Paste your Gemini API key (stored locally, never sent to server)
3. Enter your video topic
4. Select video format (Short or Long)
5. Click "Generate Script"
6. Download as PDF, copy to clipboard, or save in history

## File Structure

```
public/
├── index.html          # Main HTML file with Tailwind CSS
├── js/
│   ├── main.js        # Core script generation logic
│   └── utils.js       # PDF generation and utilities
└── manifest.json      # PWA manifest (optional)
```

## How It Works

### Script Generation Flow

1. **User Input** → Topic + Video Type
2. **Prompt Construction** → Combines system prompt with user topic
3. **Gemini API Call** → Sends to Google's Gemini 2.0 Flash
4. **Response Processing** → Formats and displays the script
5. **Storage** → Saves to browser's localStorage
6. **Export Options** → PDF, Copy, History

### Gemini API Integration

The app uses the following Gemini API endpoint:
```
https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent
```

**Parameters:**
- Model: `gemini-2.0-flash` (fast and efficient)
- Temperature: 0.7 (creative but consistent)
- Max Tokens: 2048 (enough for detailed scripts)

## Customization

### Modify Script Prompts

Edit the `PROMPTS` object in `js/main.js`:

```javascript
const PROMPTS = {
    short: `Your custom prompt for short videos...`,
    long: `Your custom prompt for long videos...`
};
```

### Change Color Scheme

Edit the gradient colors in `public/index.html`:
- Primary: `#667eea` (Purple)
- Secondary: `#764ba2` (Dark Purple)

### Add Custom Features

1. **Email Integration** - Use emailScript() function
2. **Print Feature** - Already implemented with printScript()
3. **Social Sharing** - Use shareScript() function
4. **Script Analysis** - Use analyzeScript() function

## Security Considerations

### API Key Safety

⚠️ **IMPORTANT**: The API key stored in localStorage is only for browser use:
- Never hardcode API keys in the repository
- API key is stored locally in your browser only
- You can delete the key from browser localStorage anytime
- GitHub Pages enforces HTTPS for added security

### Best Practices

1. **Rotate API Keys Regularly**
2. **Use GitHub Secrets for CI/CD** (if extending the app)
3. **Monitor API Usage** in your Google Cloud Console
4. **Set API Key Restrictions** to CORS requests only

## Features in Detail

### 📝 Roman Urdu Scripts

Scripts include authentic Roman Urdu phrases:
- "Dekho bhai" (Listen buddy)
- "Lekin masla yeh hai ke" (But the problem is)
- "Toh conclusion yeh hai ke" (So the conclusion is)
- "Agar pasand aya toh" (If you liked it then)

### 📊 Script Statistics

Generated scripts include:
- Word count
- Character count
- Estimated duration
- Reading time

### 💾 Local Storage

All your scripts are saved in browser localStorage:
- Persists across browser sessions
- Up to 20 scripts stored
- Can be cleared anytime from browser settings

### 📄 PDF Export

Professional PDF with:
- Formatted title and metadata
- Original formatting preserved
- Page numbers and footer
- Timestamped generation info

## Troubleshooting

### "API Key Invalid"
- ✅ Check your API key is correct
- ✅ Ensure the key has Gemini API enabled
- ✅ Check Google Cloud Console quotas

### "CORS Error"
- ✅ Ensure you're accessing via HTTPS
- ✅ Check if API key has proper restrictions
- ✅ Clear browser cache and try again

### Scripts Not Saving
- ✅ Check if browser localStorage is enabled
- ✅ Ensure you have enough storage space
- ✅ Try clearing old scripts from history

### PDF Download Fails
- ✅ Disable browser pop-up blockers
- ✅ Check download folder permissions
- ✅ Try a different browser

## API Limits

Google's free tier provides:
- **60 requests per minute** - per API key
- **1,500 requests per day** - per project

Monitor usage in [Google Cloud Console](https://console.cloud.google.com/)

## Environment Variables (Optional)

For advanced deployment, you can use:

```env
VITE_GEMINI_API_KEY=your_api_key_here  # Not recommended for production
```

⚠️ Never commit API keys to version control!

## Performance Optimization

The app is optimized for speed:
- ⚡ Client-side only (no server latency)
- 🔒 Uses HTTP/2 and compression via GitHub Pages
- 💾 Efficient localStorage usage
- 📦 Minimal dependencies (Tailwind, jsPDF)

## Browser Support

Fully compatible with:
- ✅ Chrome/Chromium 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Future Enhancements

Planned features:
- 🎤 Voice input support
- 🌍 Multi-language support
- 🎯 Advanced analytics
- 🤝 Community script sharing
- 📡 Cloud sync option
- 🎨 Template library

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- 📧 Email: support@techfela.com
- 💬 GitHub Issues: [Report a bug](../../issues)
- 📖 Documentation: [Full docs](../../wiki)

## Acknowledgments

- Google Gemini 2.0 Flash API
- Tailwind CSS for styling
- jsPDF for PDF generation
- Bootstrap Icons
- GitHub Pages for hosting

## Disclaimer

This tool is provided as-is. Users are responsible for:
- Obtaining and protecting their API keys
- Complying with Google Cloud Terms of Service
- Using generated content ethically and responsibly
- Respecting copyright and intellectual property rights

---

**Made with ❤️ for TechFela**

*The modern YouTube script generator for Pakistan's tech community*
