# ⚡ Quick Start - 5 Minutes to AI Chatbot

## 🚨 Your API Key Was Disabled

**What happened:** The API key you provided was compromised (now public)

**What to do:** Get a new one (takes 1 minute!)

---

## Step 1️⃣ Get New API Key (1 minute)

1. Open: https://aistudio.google.com/app/apikey
2. Click: **"Get API Key"**
3. Select: **"Create API key in new project"**
4. Copy the key (it looks like: `AIzaSy...`)
5. **Keep it secret!**

---

## Step 2️⃣ Update `.env` File (1 minute)

1. Open: `C:\Users\jadha\OneDrive\Desktop\Smart EV Charging\.env`

2. Find this line:
   ```
   GEMINI_API_KEY=your-new-gemini-api-key-here
   ```

3. Replace with your actual key:
   ```
   GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

4. Save file (Ctrl+S)

---

## Step 3️⃣ Test Connection (1 minute)

Open PowerShell and run:

```powershell
cd "C:\Users\jadha\OneDrive\Desktop\Smart EV Charging"
python test_gemini_api.py
```

Expected output:
```
✅ Gemini API Connection Successful!
📝 Response: Hello! I'm working for Smart EV Charging platform...
```

---

## Step 4️⃣ Start the App (1 minute)

```powershell
python app.py
```

You should see:
```
✅ Gemini API configured successfully
...
Running on http://localhost:5000
```

---

## Step 5️⃣ Test Chatbot (1 minute)

1. Open browser: http://localhost:5000
2. Login with: user1 / password123
3. Go to: "Ask AI Assistant" (or `/user/chat`)
4. Try asking:
   - "What's the cheapest charging station?"
   - "Which stations have green energy?"
   - "I'm running low on battery!"

**Expected:** Intelligent AI responses! 🤖

---

## ✅ You're Done!

Your Smart EV Charging Platform with Gemini AI is now live! 🚀

### What Works:
- ✅ AI Chatbot (24/7 support)
- ✅ Smart Recommendations
- ✅ Natural Language Search
- ✅ All other features

### Next:
- Explore the demo
- Try all features
- Have fun! 🎉

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "API key was reported as leaked" | Get NEW key from Google AI Studio |
| "Still getting fallback responses" | Restart `python app.py` |
| "ModuleNotFoundError: google.genai" | Run `pip install -U google-genai` |
| "API key not found" | Verify `.env` file exists in project root |

---

**You've got this!** 💪 Just get that new API key and you're golden! ✨
