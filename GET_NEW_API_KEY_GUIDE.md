# 🔑 Getting a NEW Gemini API Key - Step by Step

## ⚠️ Why The Old Key Doesn't Work

The API key you provided (`AIzaSyDTML0wuZQe9yDufXQJgZ-zrauIWcSj1lQ`) has been **permanently disabled by Google** with error:

```
403 PERMISSION_DENIED
Your API key was reported as leaked. Please use another API key.
```

**This key cannot be reactivated.** Google has permanently blacklisted it.

---

## 📖 How to Get a NEW Valid Key (5 minutes)

### Step 1: Open Google AI Studio
- **URL:** https://aistudio.google.com/app/apikey
- **Open in browser** (Chrome, Edge, Firefox, etc.)

### Step 2: Sign In
- If not already signed in, use your Google account
- Accept any permissions requested

### Step 3: Click "Get API Key"
- You'll see a button labeled **"Get API Key"**
- Click it

### Step 4: Create API Key
- A dialog will appear with options:
  - Option A: "Create API key in new project" ← **Choose This**
  - Option B: "Create API key in existing project"

- Click **"Create API key in new project"**

### Step 5: Copy Your NEW Key
- Google will display your new API key
- It will look like: `AIzaSy...` (but a different one)
- Click **"Copy"** button or manually select and copy

### Step 6: Keep It Private
- ⚠️ **NEVER** share this key publicly
- ⚠️ **NEVER** commit it to git
- ⚠️ **NEVER** post it in messages
- Store it **ONLY in `.env` file**

---

## ✅ Update Your `.env` File

1. Open: `C:\Users\jadha\OneDrive\Desktop\Smart EV Charging\.env`

2. You'll see:
   ```
   GEMINI_API_KEY=YOUR_NEW_API_KEY_FROM_GOOGLE_HERE
   ```

3. Replace the placeholder with your NEW key:
   ```
   GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

4. **Save the file** (Ctrl+S)

---

## 🧪 Test Your NEW Key

Run this command to verify:

```powershell
cd "C:\Users\jadha\OneDrive\Desktop\Smart EV Charging"
python test_gemini_api.py
```

### Expected Outputs:

**✅ SUCCESS:**
```
✅ Gemini API Connection Successful!
📝 Response: Hello! I'm working for Smart EV Charging platform...
```

**❌ FAILURE:**
```
❌ Error: 403 PERMISSION_DENIED. Your API key was reported as leaked.
```
→ This means the key is also compromised; get another one

**❌ FAILURE:**
```
❌ Error: 400 API_KEY_INVALID. API key not valid.
```
→ Make sure you copied the FULL key correctly

---

## 🚀 Once Test Succeeds

Run the app:
```powershell
python app.py
```

Visit: http://localhost:5000/user/chat

---

## 🆘 Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "API key was reported as leaked" | Key is compromised | Get a brand NEW key |
| "API key not valid" | Key is malformed | Copy the FULL key correctly |
| "API key not found" | `.env` not in project root | Verify file location |
| "Still fallback responses" | `.env` not saved or app not restarted | Save and restart app |

---

## ✨ Key Points

✅ The new key must be from https://aistudio.google.com/app/apikey
✅ Make sure it's created in a **NEW project**
✅ Copy the ENTIRE key string
✅ Update `.env` file (not in code!)
✅ Save `.env` and test
✅ Restart `app.py` after updating

---

**You're just one API key away from having a fully functional AI platform!** 🚀

Once you get the new key and update `.env`, everything will work perfectly!
