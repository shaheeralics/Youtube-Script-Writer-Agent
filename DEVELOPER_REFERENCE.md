# Developer Quick Reference

## API Endpoints

### Gemini API
```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}
```

**Response:**
```json
{
    "candidates": [
        {
            "content": {
                "parts": [
                    {
                        "text": "Generated script content here..."
                    }
                ]
            }
        }
    ]
}
```

---

## JavaScript API Reference

### Script Generation
```javascript
// Generate a script
generateScript()

// Call Gemini API directly
callGeminiAPI(apiKey, prompt)

// Display script with stats
displayScript(script, topic, videoType)
```

### History Management
```javascript
// Add to history
addToHistory(entry)

// Load from storage
loadHistoryFromStorage()

// Save to storage
saveHistoryToStorage()

// Load script from history
loadScriptFromHistory(index)

// Delete from history
deleteFromHistory(event, index)
```

### Export Functions
```javascript
// Download as PDF
downloadScriptPDF()

// Download as text
downloadScriptAsText()

// Download as markdown
downloadScriptAsMarkdown()

// Print script
printScript()

// Share script
shareScript()

// Email script
emailScript()
```

### Analysis Functions
```javascript
// Analyze script content
analyzeScript(script)
// Returns: {totalWords, totalCharacters, sentences, readingTimeMinutes, uniqueWords}

// Extract keywords
extractKeywords(script, count)

// Generate summary
generateScriptSummary(script, maxLength)

// Generate table of contents
generateTableOfContents(script)
```

---

## LocalStorage Keys

```javascript
localStorage.getItem('geminiApiKey')           // API key
localStorage.getItem('scriptHistory')          // All scripts
localStorage.getItem('totalScriptsGenerated')  // Counter
```

---

## Customization Examples

### Change Prompt
```javascript
// In js/main.js
const PROMPTS = {
    short: `Your custom prompt here...`,
    long: `Your custom prompt here...`
};
```

### Change Colors
```css
/* In index.html <style> */
.gradient-bg {
    background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
}
```

### Add New Button
```html
<!-- In index.html -->
<button onclick="yourFunction()" class="...">
    <i class="bi bi-icon-name"></i> Label
</button>

<!-- In js/main.js -->
function yourFunction() {
    // Your code here
}
window.yourFunction = yourFunction;
```

---

## Performance Tips

### Reduce Bundle Size
- ✅ Use CDN for libraries
- ✅ Lazy load heavy scripts
- ✅ Minify CSS/JS in production

### Optimize API Calls
- ✅ Cache responses
- ✅ Batch requests
- ✅ Handle rate limits

### Improve UX
- ✅ Show loading states
- ✅ Add error handling
- ✅ Provide feedback

---

## Testing Checklist

- [ ] Works on Chrome
- [ ] Works on Firefox
- [ ] Works on Safari
- [ ] Works on Edge
- [ ] Mobile responsive
- [ ] Touch-friendly
- [ ] Offline mode works
- [ ] PDF generation works
- [ ] Copy to clipboard works
- [ ] History saves correctly
- [ ] API error handling works
- [ ] Console no errors/warnings

---

## Deployment Commands

```bash
# Commit changes
git add .
git commit -m "Your message"

# Push to GitHub
git push origin main

# Deployment starts automatically
# Check status in Actions tab

# View deployment logs
# Go to: Settings → Deployments
```

---

## Common Changes

### Update Greeting
```javascript
// In js/main.js - generate_script function
const greeting = "Assalam o Alaikum!";
```

### Add More Video Types
```javascript
// In PROMPTS object
const PROMPTS = {
    shorts: `...`,     // New
    reels: `...`,      // New
    long: `...`
};
```

### Modify PDF Header
```javascript
// In utils.js - downloadScriptPDF function
doc.text('Your Custom Header', margin, yPosition);
```

---

## Browser Console Tricks

```javascript
// Check if online
navigator.onLine

// Check localStorage space used
new Blob(Object.values(localStorage)).size

// Clear all data
localStorage.clear()

// Export data
JSON.stringify(JSON.parse(localStorage.getItem('scriptHistory')))

// Unregister service worker
navigator.serviceWorker.getRegistrations().then(r => r.forEach(rr => rr.unregister()))
```

---

## Security Best Practices

❌ **Don't:**
- Commit API keys
- Use dynamic API keys
- Store sensitive data in localStorage
- Make requests without HTTPS

✅ **Do:**
- Use environment files locally
- Store only non-sensitive data
- HTTPS everywhere (GitHub Pages enforces this)
- Validate all inputs
- Handle errors gracefully

---

## Resources

- [Tailwind CSS Docs](https://tailwindcss.com)
- [Bootstrap Icons](https://icons.getbootstrap.com)
- [jsPDF Docs](https://github.com/parallax/jsPDF)
- [Google Gemini API](https://ai.google.dev)
- [MDN Web Docs](https://developer.mozilla.org)

---

**Happy Coding! 🚀**
