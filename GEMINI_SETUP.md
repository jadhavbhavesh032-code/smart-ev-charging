# Google Gemini API Integration Guide

## Overview
The Smart EV Charging platform now uses Google Gemini API to provide intelligent, AI-powered charging recommendations with personalized explanations.

## Setup Instructions

### 1. Get Gemini API Key
- Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
- Click "Get API Key"
- Create a new API key
- Copy the key (keep it secure!)

### 2. Install Required Package
```bash
pip install google-generativeai
```

Or update your environment:
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variable

**Option A: Windows PowerShell**
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
python app.py
```

**Option B: Windows Command Prompt**
```cmd
set GEMINI_API_KEY=your-api-key-here
python app.py
```

**Option C: Create a .env file** (recommended for development)
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your-api-key-here
```

Then install python-dotenv:
```bash
pip install python-dotenv
```

Update `app.py` to load the .env file:
```python
from dotenv import load_dotenv
load_dotenv()
```

### 4. Verify Installation
Run the app and test the AI recommendations:
1. Login as a user
2. Go to "AI Recommendations" 
3. Enter battery percentage and distance
4. You should see AI-powered explanations

## Features

### What Gemini AI Does:
- **Intelligent Recommendations**: Analyzes multiple factors beyond basic scoring
- **Personalized Explanations**: Explains why a station is recommended
- **Key Benefits**: Lists top 2-3 reasons to choose the station
- **Charging Tips**: Provides practical advice for optimal charging

### Fallback Mode:
If the API key is not set or API fails:
- System automatically falls back to basic recommendations
- Still provides helpful explanations based on algorithms
- No disruption to user experience

## API Response Format

The enhanced recommender now returns:
```python
best_station, explanation = recommend_station(battery, distance, stations)
```

Example output:
```
Station Name: Central Charging Hub

This station offers an optimal balance of:
• Accessibility with 5 available chargers
• Eco-friendly energy sources (Score: 8/10)
• Competitive pricing at ₹8/kWh

Key Benefits:
• 100% renewable energy
• Fast charging capability
• Rewards program available

Tip: Charge during off-peak hours (8-10 AM) for 10% discount!
```

## Code Changes Made

### 1. Enhanced `ai/recommender.py`
- Integrated Google Gemini API
- Added `_generate_ai_explanation()` function
- Added fallback explanation generator
- Improved error handling and logging

### 2. Updated `routes/station_routes.py`
- Modified `/user/recommend` route to handle new return format
- Now passes explanation to template

### 3. Updated `templates/recommend_result.html`
- Displays AI Analysis section
- Shows formatted explanation with proper styling
- Replaced static recommendations with dynamic AI content

### 4. Updated `requirements.txt`
- Added `google-generativeai>=0.3.0`

## Testing

### Test without API key (fallback mode):
```bash
python app.py
# Navigate to AI Recommendations
# Should still work with basic recommendations
```

### Test with API key:
```bash
$env:GEMINI_API_KEY="your-key"
python app.py
# Navigate to AI Recommendations
# Should show AI-powered explanations
```

## Troubleshooting

### "GEMINI_API_KEY not found" 
- Ensure environment variable is set correctly
- Check spelling: `GEMINI_API_KEY` (case-sensitive)
- Restart terminal/IDE after setting variable

### "API returned error"
- Verify API key is valid
- Check API quota on Google AI Studio dashboard
- Ensure internet connection is active

### Slow recommendations
- Gemini API might take 2-3 seconds
- This is normal for AI generation
- Consider implementing caching for frequently requested combinations

## Future Enhancements

1. **Caching**: Cache recommendations for common battery/distance combinations
2. **User Preferences**: Learn user preferences (eco-friendly, budget-conscious, etc.)
3. **Predictive Analysis**: Predict charging patterns and suggest optimal times
4. **Multi-language Support**: Generate recommendations in user's language
5. **Batch Recommendations**: Return top 3-5 stations with explanations

## Security Notes

- Never commit API keys to version control
- Use environment variables for production
- Rotate API keys periodically
- Monitor API usage on Google AI Studio dashboard
