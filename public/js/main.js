// ============================================
// YouTube Script Generator - Main Logic
// ============================================

// Prompts for different video types
const PROMPTS = {
    short: `You are a creative scriptwriter for TechFela YouTube channel that creates engaging, humorous content in Roman Urdu for a Pakistani audience. The scripts should be 60-90 seconds long.

Create a SHORT format (60-90 seconds) YouTube script following this structure:
- (0-15 seconds): Hook - Make viewers want to stay
- (15-30 seconds): Introduce the topic with a question or statement in Roman Urdu
- (30-45 seconds): Main content/explanation
- (45-60 seconds): The twist or surprising fact
- (60-75 seconds): Call to action (like, subscribe, comment)
- (75-90 seconds): Closing statement with personality

Make it funny, relatable, and use common Roman Urdu phrases like "Dekho bhai", "Lekin masla yeh hai ke", "Toh conclusion yeh hai ke", "Agar pasand aya toh".
Include emojis where appropriate to make the script more engaging.

Topic to cover:`,
    long: `You are a creative scriptwriter for TechFela YouTube channel that creates engaging, humorous content in Roman Urdu for a Pakistani audience. The scripts should be 3-6 minutes long (approximately 450-900 words).

Create a LONG format (3-6 minutes) YouTube script following this structure:
- (0-30 seconds): Greeting and introduction in Roman Urdu
- (30-90 seconds): Background on the topic
- (90-150 seconds): Main benefits/advantages (3+ points with explanations)
- (150-210 seconds): Disadvantages or challenges
- (210-270 seconds): Future prospects in Pakistan
- (270-330 seconds): Practical steps viewers can take
- (330-360 seconds): Call to action and closing

Use natural Roman Urdu language, include "Assalam o Alaikum", humor for Pakistani tech audience, and make it educational yet entertaining.
Include timestamps in your response for better editing.
Add personality with phrases like "Dosto", "Bhai", "Acha suno", etc.

Topic to cover:`
};

// Global state
const AppState = {
    scriptHistory: [],
    currentScript: null,
    isGenerating: false,
};

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadHistoryFromStorage();
    setupAutoSaveApiKey();
    setupPWAInstallPrompt();
});

// PWA Install Prompt
let deferredPrompt;
function setupPWAInstallPrompt() {
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        
        // Show install button if PWA can be installed
        const installBtn = document.getElementById('installPWABtn');
        if (installBtn) {
            installBtn.style.display = 'block';
            installBtn.addEventListener('click', () => {
                if (deferredPrompt) {
                    deferredPrompt.prompt();
                    deferredPrompt.userChoice.then((choiceResult) => {
                        if (choiceResult.outcome === 'accepted') {
                            console.log('PWA installed');
                        }
                        deferredPrompt = null;
                    });
                }
            });
        }
    });

    window.addEventListener('appinstalled', () => {
        console.log('PWA installed successfully');
        deferredPrompt = null;
    });
}

// ============================================
// Event Listeners
// ============================================

function initializeEventListeners() {
    // Generate Script Button
    document.getElementById('generateBtn').addEventListener('click', generateScript);

    // New Script Button
    document.getElementById('newScriptBtn').addEventListener('click', resetForm);

    // Download PDF Button
    document.getElementById('downloadPdfBtn').addEventListener('click', downloadScriptPDF);

    // Copy Button
    document.getElementById('copyBtn').addEventListener('click', copyScriptToClipboard);

    // History Button
    document.getElementById('historyBtn').addEventListener('click', showHistoryModal);

    // Close History Modal
    document.getElementById('closeHistoryModal').addEventListener('click', hideHistoryModal);

    // Topic Input - Allow Enter key to generate
    document.getElementById('topicInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            generateScript();
        }
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + G = Generate
        if ((e.ctrlKey || e.metaKey) && e.key === 'g') {
            e.preventDefault();
            generateScript();
        }
        
        // Ctrl/Cmd + N = New
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            e.preventDefault();
            resetForm();
        }
        
        // Ctrl/Cmd + H = History
        if ((e.ctrlKey || e.metaKey) && e.key === 'h') {
            e.preventDefault();
            showHistoryModal();
        }
        
        // Ctrl/Cmd + Shift + S = Save/Download PDF
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'S') {
            e.preventDefault();
            downloadScriptPDF();
        }
        
        // Ctrl/Cmd + Shift + C = Copy
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'C') {
            e.preventDefault();
            copyScriptToClipboard();
        }
    });

    // Close modal when clicking outside
    document.getElementById('historyModal').addEventListener('click', (e) => {
        if (e.target === document.getElementById('historyModal')) {
            hideHistoryModal();
        }
    });
}

// ============================================
// Generate Script
// ============================================

async function generateScript() {
    const apiKey = document.getElementById('apiKey').value.trim();
    const topic = document.getElementById('topicInput').value.trim();
    const videoType = document.querySelector('input[name="videoType"]:checked').value;

    // Validation
    if (!apiKey) {
        showError('Please enter your Gemini API key');
        return;
    }

    if (!topic) {
        showError('Please enter a topic');
        return;
    }

    if (topic.length > 200) {
        showError('Topic is too long (max 200 characters)');
        return;
    }

    // Show loading state
    setLoading(true);
    clearOutput();

    try {
        // Construct the prompt
        const prompt = PROMPTS[videoType] + '\n' + topic;

        // Call Gemini API
        const response = await callGeminiAPI(apiKey, prompt);

        if (!response) {
            showError('Failed to generate script. Please check your API key and try again.');
            setLoading(false);
            return;
        }

        // Process and display the script
        displayScript(response, topic, videoType);

        // Add to history
        addToHistory({
            topic: topic,
            videoType: videoType,
            script: response,
            timestamp: new Date().toLocaleString(),
            wordCount: response.split(/\s+/).length,
        });

        // Show success
        document.getElementById('outputActions').style.display = 'flex';

        setLoading(false);
    } catch (error) {
        console.error('Error:', error);
        showError(`Error: ${error.message}`);
        setLoading(false);
    }
}

// ============================================
// Gemini API Call
// ============================================

async function callGeminiAPI(apiKey, prompt) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

    const requestBody = {
        contents: [
            {
                parts: [
                    {
                        text: prompt
                    }
                ]
            }
        ],
        generationConfig: {
            temperature: 0.7,
            topK: 40,
            topP: 0.95,
            maxOutputTokens: 2048,
        }
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error?.message || `API Error: ${response.status}`);
        }

        const data = await response.json();

        if (data.candidates && data.candidates[0] && data.candidates[0].content) {
            return data.candidates[0].content.parts[0].text;
        }

        throw new Error('Invalid API response format');
    } catch (error) {
        throw error;
    }
}

// ============================================
// Display Script
// ============================================

function displayScript(script, topic, videoType) {
    const contentDiv = document.getElementById('scriptContent');
    const emptyDiv = document.getElementById('emptyState');

    // Populate content
    document.getElementById('scriptTitle').textContent = `📝 Script for: ${topic} (${videoType === 'short' ? 'Short' : 'Long'} Format)`;
    document.getElementById('scriptText').textContent = script;

    // Calculate statistics
    const wordCount = script.split(/\s+/).length;
    const charCount = script.length;
    
    document.getElementById('wordCount').textContent = wordCount;
    document.getElementById('charCount').textContent = charCount;
    
    // Estimate duration
    const estimatedSeconds = videoType === 'short' ? 75 : 300;
    document.getElementById('duration').textContent = formatDuration(estimatedSeconds);

    // Store current script
    AppState.currentScript = { script, topic, videoType, wordCount, charCount };

    // Show content, hide empty
    contentDiv.style.display = 'block';
    emptyDiv.style.display = 'none';
}

// ============================================
// UI State Management
// ============================================

function setLoading(isLoading) {
    AppState.isGenerating = isLoading;
    document.getElementById('loadingState').style.display = isLoading ? 'block' : 'none';
    document.getElementById('generateBtn').disabled = isLoading;
    document.getElementById('generateBtn').style.opacity = isLoading ? '0.6' : '1';
}

function showError(message) {
    const errorDiv = document.getElementById('errorState');
    document.getElementById('errorMessage').textContent = message;
    errorDiv.style.display = 'flex';
    document.getElementById('scriptContent').style.display = 'none';
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('outputActions').style.display = 'none';
}

function clearOutput() {
    document.getElementById('errorState').style.display = 'none';
    document.getElementById('scriptContent').style.display = 'none';
    document.getElementById('emptyState').style.display = 'block';
    document.getElementById('outputActions').style.display = 'none';
}

function resetForm() {
    document.getElementById('topicInput').value = '';
    document.querySelector('input[name="videoType"][value="short"]').checked = true;
    clearOutput();
    AppState.currentScript = null;
}

// ============================================
// Copy to Clipboard
// ============================================

function copyScriptToClipboard() {
    if (!AppState.currentScript) {
        showError('No script to copy');
        return;
    }

    const script = AppState.currentScript.script;
    navigator.clipboard.writeText(script).then(() => {
        const copyBtn = document.getElementById('copyBtn');
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = '<i class="bi bi-check-lg"></i> Copied!';
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
        }, 2000);
    }).catch(err => {
        showError('Failed to copy to clipboard');
    });
}

// ============================================
// History Management
// ============================================

function addToHistory(entry) {
    AppState.scriptHistory.unshift(entry);
    // Keep only last 20 scripts
    if (AppState.scriptHistory.length > 20) {
        AppState.scriptHistory.pop();
    }
    saveHistoryToStorage();
    updateHistoryDisplay();
}

function loadHistoryFromStorage() {
    const stored = localStorage.getItem('scriptHistory');
    if (stored) {
        try {
            AppState.scriptHistory = JSON.parse(stored);
        } catch (e) {
            console.error('Failed to load history:', e);
        }
    }
}

function saveHistoryToStorage() {
    localStorage.setItem('scriptHistory', JSON.stringify(AppState.scriptHistory));
}

function updateHistoryDisplay() {
    const historyList = document.getElementById('historyList');
    const modalList = document.getElementById('modalHistoryList');

    if (AppState.scriptHistory.length === 0) {
        historyList.innerHTML = '<p class="text-gray-500 text-center">No scripts generated yet</p>';
        modalList.innerHTML = '<p class="text-gray-500 text-center">No scripts generated yet</p>';
        return;
    }

    let html = '';
    AppState.scriptHistory.forEach((script, index) => {
        html += `
            <div class="bg-gray-50 p-4 rounded-lg hover:bg-gray-100 cursor-pointer transition" onclick="loadScriptFromHistory(${index})">
                <div class="flex justify-between items-start">
                    <div>
                        <p class="font-semibold text-gray-900">${truncateText(script.topic, 40)}</p>
                        <p class="text-xs text-gray-500">${script.timestamp}</p>
                        <p class="text-xs text-gray-600 mt-1">
                            <span class="bg-purple-100 text-purple-800 px-2 py-0.5 rounded">${script.videoType}</span>
                            <span class="ml-2">${script.wordCount} words</span>
                        </p>
                    </div>
                    <button onclick="deleteFromHistory(event, ${index})" class="text-red-400 hover:text-red-600 text-lg">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </div>
        `;
    });

    historyList.innerHTML = html;
    modalList.innerHTML = html;
}

function loadScriptFromHistory(index) {
    const script = AppState.scriptHistory[index];
    if (!script) return;

    document.getElementById('topicInput').value = script.topic;
    document.querySelector(`input[name="videoType"][value="${script.videoType}"]`).checked = true;
    displayScript(script.script, script.topic, script.videoType);
    document.getElementById('outputActions').style.display = 'flex';
}

function deleteFromHistory(event, index) {
    event.stopPropagation();
    AppState.scriptHistory.splice(index, 1);
    saveHistoryToStorage();
    updateHistoryDisplay();
}

function showHistoryModal() {
    document.getElementById('historyModal').classList.remove('hidden');
    updateHistoryDisplay();
}

function hideHistoryModal() {
    document.getElementById('historyModal').classList.add('hidden');
}

// ============================================
// API Key Management
// ============================================

function setupAutoSaveApiKey() {
    const apiKeyInput = document.getElementById('apiKey');
    const savedKey = localStorage.getItem('geminiApiKey');
    if (savedKey) {
        apiKeyInput.value = savedKey;
    }

    apiKeyInput.addEventListener('change', () => {
        localStorage.setItem('geminiApiKey', apiKeyInput.value);
    });
}

// ============================================
// Utility Functions
// ============================================

function truncateText(text, length) {
    return text.length > length ? text.substring(0, length) + '...' : text;
}

function formatDuration(seconds) {
    if (seconds < 60) return `${seconds}s`;
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes}m ${secs}s`;
}

// Export functions for HTML
window.generateScript = generateScript;
window.resetForm = resetForm;
window.downloadScriptPDF = downloadScriptPDF;
window.copyScriptToClipboard = copyScriptToClipboard;
window.showHistoryModal = showHistoryModal;
window.hideHistoryModal = hideHistoryModal;
window.loadScriptFromHistory = loadScriptFromHistory;
window.deleteFromHistory = deleteFromHistory;
