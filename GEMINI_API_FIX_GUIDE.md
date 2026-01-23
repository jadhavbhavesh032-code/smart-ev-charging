# 🔧 Gemini API Setup Guide

## Problem
The AI chatbot is returning the same fallback response for all queries because the **GEMINI_API_KEY** environment variable is not set.

## Solution

### Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Get API Key"**
3. Choose **"Create API key in new project"** or select existing project
4. Copy the API key (looks like: `AIzaSy...`)
5. Keep it safe and don't share it!

---

### Step 2: Set Up Environment Variable

#### **Option A: Using .env File (Recommended for Development)**

1. Create a `.env` file in the project root:
   ```
   C:\Users\jadha\OneDrive\Desktop\Smart EV Charging\.env
   ```

2. Add this line:
   ```
   GEMINI_API_KEY=your-api-key-here
   ```

3. Install python-dotenv if not already installed:
   ```powershell
   pip install python-dotenv
   ```

4. The code now automatically loads from `.env` file ✅

---

#### **Option B: Using Environment Variable (Windows)**

**Method 1: PowerShell (Session Only)**
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
python app.py
```

**Method 2: Command Prompt (Session Only)**
```cmd
set GEMINI_API_KEY=your-api-key-here
python app.py
```

**Method 3: Permanent (Windows System)**
1. Press `Win + X` → Choose "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Click "New" under User variables
5. Variable name: `GEMINI_API_KEY`
6. Variable value: `your-api-key-here`
7. Click OK and restart your terminal

---

### Step 3: Verify Setup

Run this command to test:

```powershell
cd "C:\Users\jadha\OneDrive\Desktop\Smart EV Charging"

# Check if key is loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(f'API Key loaded: {\"✅\" if os.getenv(\"GEMINI_API_KEY\") else \"❌\"}')"

# Or check environment variable
echo $env:GEMINI_API_KEY
```

If you see your API key starting with `AIza...`, you're good! ✅

---

### Step 4: Update requirements.txt

Ensure `python-dotenv` is in your requirements:

```bash
pip install -r requirements.txt
```

Or add manually:
```bash
pip install python-dotenv
```

---

### Step 5: Test the Chatbot

1. Start the Flask app:
   ```powershell
   python app.py
   ```

2. Go to: `http://localhost:5000/user/chat`

3. Try these queries:
   - ✅ "What's the cheapest station?"
   - ✅ "Which stations have green energy?"
   - ✅ "I'm running low on battery, help!"

4. **You should now get intelligent AI responses instead of the fallback message!**

---

## What's New in the Code

### Updated Files:

1. **`.env.example`** - Template for environment configuration
2. **`ai/chatbot.py`** - Enhanced with:
   - `load_dotenv()` support
   - Better error logging with emoji indicators
   - Debug messages to track API calls
   - Improved error messages

### Logging Indicators:

- ✅ `Gemini API configured successfully` - Everything working
- ⚠️ `GEMINI_API_KEY not set` - No API key (will use fallback)
- 🔄 `Sending message to Gemini API` - Request in progress
- ❌ `Chatbot API error` - API call failed (falling back to keywords)

---

## Troubleshooting

### Issue: Still getting fallback responses?

**Check 1: Is GEMINI_API_KEY set?**
```powershell
echo $env:GEMINI_API_KEY
```
Should output your API key (or use `.env` file)

**Check 2: Is `.env` file in the right location?**
```
✅ Correct: C:\Users\jadha\OneDrive\Desktop\Smart EV Charging\.env
❌ Wrong: C:\Users\jadha\OneDrive\Desktop\.env
```

**Check 3: Restart Flask**
- Stop Flask (Ctrl+C)
- Start again: `python app.py`
- Changes to `.env` require restart

**Check 4: Check logs**
- Flask will show debug messages like:
  - `✅ Gemini API configured successfully`
  - `❌ Failed to configure Gemini API`
  - `🔄 Sending message to Gemini API`

### Issue: "ModuleNotFoundError: No module named 'dotenv'"

```powershell
pip install python-dotenv
```

### Issue: API Key invalid or quota exceeded?

1. Check your API key is correct (starts with `AIza...`)
2. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
3. Verify key hasn't expired
4. Check usage quota in Google Cloud Console

---

## Security Best Practices

⚠️ **DO NOT:**
- ❌ Commit `.env` file to git
- ❌ Share your API key publicly
- ❌ Hardcode API key in source files

✅ **DO:**
- ✅ Add `.env` to `.gitignore`
- ✅ Use `.env` file for development
- ✅ Use secure environment management in production (AWS Secrets Manager, Azure Key Vault, etc.)
- ✅ Rotate API keys periodically

---

## Next Steps

After setting up Gemini API:

1. ✅ Test chatbot responses
2. ✅ Check AI recommendations feature (`/user/recommend`)
3. ✅ Try natural language search (`/user/nl-search`)
4. ✅ Test all 3 Gemini integrations in the platform

---

## Alternative: Fallback Mode

If you can't set up Gemini API right now:

The platform still works! All features with fallback:
- Chatbot uses keyword matching
- Recommendations use algorithm
- NL Search uses basic filters

Performance is reduced but functional. Once you add the API key, all AI features unlock automatically! 🚀

---

**Questions?** Check `GEMINI_SETUP.md` or `AI_FEATURES_GUIDE.md` for more details.
