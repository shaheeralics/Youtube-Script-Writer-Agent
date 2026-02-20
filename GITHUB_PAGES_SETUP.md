# GitHub Pages Deployment Guide

## Quick Start (5 Minutes)

### Step 1: Enable GitHub Pages
```
Repository Settings → Pages → Source: Deploy from a branch → Main → /public
```

### Step 2: Add Your API Key
When you open the app:
1. Get free Gemini API key at: https://ai.google.dev
2. Paste it in the app (stored locally only)
3. Start generating scripts!

### Step 3: Your URL
```
https://YOUR_USERNAME.github.io/Youtube-Script-Writer/
```

---

## Detailed Configuration

### Repository Structure
```
Youtube-Script-Writer/
├── public/                 # GitHub Pages content root
│   ├── index.html         # Main app (Tailwind CSS)
│   ├── manifest.json      # PWA manifest
│   ├── sw.js              # Service Worker
│   └── js/
│       ├── main.js        # Core functionality
│       └── utils.js       # Utilities & PDF
├── .github/
│   └── workflows/
│       └── deploy.yml     # Auto-deployment
└── README_GITHUB_PAGES.md # This guide
```

### GitHub Settings

1. **Go to Settings → Pages**
   - Source: Deploy from a branch
   - Branch: main (or master)
   - Directory: /public

2. **Enable HTTPS (Automatic)**
   - GitHub Pages automatically enables HTTPS
   - All API calls are secure

3. **Custom Domain (Optional)**
   - Add CNAME file to public folder with your domain
   - Update DNS records as instructed

### Build Process

Automatic deployment happens when:
- Files in `/public` folder are pushed
- GitHub Actions workflow triggers
- Deployment completes in 1-2 minutes

### API Key Security

**✅ Safe:**
- Keys stored in browser localStorage
- Never transmitted except to Google API
- Can be cleared anytime

**❌ Avoid:**
- Hardcoding keys in HTML/JS
- Committing .env files
- Sharing keys in repositories

---

## Features & Technologies

### Frontend Stack
- **HTML5/CSS3** - Semantic markup
- **Tailwind CSS** - Utility-first styling
- **JavaScript ES6+** - Modern JavaScript
- **jsPDF** - PDF generation
- **Bootstrap Icons** - Icon library

### APIs Used
- **Google Gemini 2.0 Flash** - AI script generation
- **GitHub Pages** - Hosting
- **localStorage** - Client-side storage

### Performance
- No build step needed
- CDN-delivered CSS/JS
- Service Worker for offline support
- Minimal JavaScript (30KB gzipped)

---

## Customization

### Change App Title
Edit `public/index.html`:
```html
<title>🎬 Your Custom Title</title>
```

### Modify Prompts
Edit `public/js/main.js`:
```javascript
const PROMPTS = {
    short: `Your custom prompt...`,
    long: `Your custom prompt...`
};
```

### Change Colors
Edit CSS in `public/index.html`:
- Primary: `#667eea` → `#your-color`
- Secondary: `#764ba2` → `#your-color`

### Add Features
Examples in `public/js/utils.js`:
- `downloadScriptAsText()`
- `printScript()`
- `shareScript()`
- `analyzeScript()`

---

## Troubleshooting

### App Not Showing
**Solution:**
- Wait 2-3 minutes for first deployment
- Hard refresh (Ctrl+Shift+R)
- Clear browser cache

### API Quota Exceeded
**Solution:**
- Check usage in Google Cloud Console
- Wait for quota reset (24 hours)
- Or upgrade to paid plan

### CORS Errors
**Solution:**
- Ensure accessing via HTTPS
- Check API key restrictions
- Try incognito mode

### PDF Not Downloading
**Solution:**
- Disable pop-up blockers
- Check browser download settings
- Try different browser

---

## Cost

✅ **Completely FREE:**
- GitHub Pages hosting: $0
- Gemini API: Free tier (60 req/min, 1500/day)
- No credit card required

---

## Monitoring

### Track API Usage
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. View → API → Quota metrics

### Monitor Deployment
1. Go to Repository → Deployments
2. See deployment history
3. Check for errors in logs

---

## Production Checklist

- [ ] Test on Chrome, Firefox, Safari
- [ ] Test on Mobile (iOS/Android)
- [ ] Test PDF generation
- [ ] Test history save/load
- [ ] Test with invalid API key
- [ ] Test without internet (offline)
- [ ] Check console for errors
- [ ] Verify HTTPS connection

---

## Rollback

If something breaks:

```bash
# Revert to previous commit
git revert HEAD

# Or restore specific file
git checkout HEAD~ public/index.html
```

---

## Advanced: Custom Domain

1. **Add CNAME to public folder:**
   ```
   your-domain.com
   ```

2. **Update DNS Records:**
   - Add CNAME: `yourusername.github.io`
   - Or add A records (see GitHub docs)

3. **Wait for DNS propagation** (5-48 hours)

4. **Verify in Settings → Pages**

---

## Support & Issues

- 📧 Create an issue: [GitHub Issues](../../issues)
- 💬 Discussions: [GitHub Discussions](../../discussions)
- 📖 Wiki: [Project Wiki](../../wiki)

---

**Last Updated:** February 2026  
**Status:** ✅ Production Ready
