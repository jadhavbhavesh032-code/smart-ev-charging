# Advanced AI Features Implementation Guide

## Overview
This document covers the four major AI-powered features implemented in the Smart EV Charging platform using Google Gemini API:

1. **AI Chatbot** - 24/7 virtual assistant
2. **Predictive Analytics** - Forecast demand, peak times, pricing
3. **Personalized Insights** - User-specific charging analytics
4. **Natural Language Query System** - "Find green stations with fast charging"

---

## 1. AI Chatbot Assistant

### Location
- **Module:** `ai/chatbot.py`
- **Route:** `/user/chat`
- **Template:** `templates/chat_interface.html`

### Features
- **24/7 Support:** Answer questions about stations, pricing, charging, troubleshooting
- **Context-Aware:** Remembers conversation history
- **Smart Fallback:** Works even without Gemini API (uses keyword matching)
- **Multi-Topic:** Handles pricing, eco-friendly options, technical issues, bookings

### How It Works

```python
from ai.chatbot import chat_with_bot

# Single message or conversation
response, is_error = chat_with_bot(
    user_message="What stations have fast charging?",
    conversation_history=[
        ("user", "Hi there"),
        ("bot", "Hello! How can I help?")
    ]
)
```

### Topics Covered
- Station finder queries
- Pricing and billing
- Charging recommendations
- Payment issues
- Technical troubleshooting
- Environmental benefits
- Charging queue info
- Account help

### UI Features
- Beautiful chat interface with message bubbles
- Example query buttons
- Helpful tips section
- 24/7 availability badge

---

## 2. Predictive Analytics

### Location
- **Module:** `ai/analytics.py`
- **Routes:** 
  - `/user/station-analytics/<station_name>` - View station analytics
  - Integrated into station listings

### Functions

#### `get_peak_hours(station_name)`
Predicts busiest hours based on historical data
```python
hours_data = get_peak_hours("Central Hub")
# Returns: [{hour: "09:00", count: 45, intensity: 8, is_peak: True}, ...]
```

#### `get_station_demand_forecast(station_name, days_ahead=7)`
Forecasts next 7 days demand
```python
forecast = get_station_demand_forecast("Central Hub")
# Returns: [{date: "2026-01-21", day: "Tuesday", expected_sessions: 50, confidence: "high"}, ...]
```

#### `get_price_trend(station_name)`
Analyzes price trends
```python
trend = get_price_trend("Central Hub")
# Returns: {
#     current_price: 8.50,
#     historical_avg: 8.20,
#     trend: "stable",
#     recommendation: "Prices are stable"
# }
```

#### `get_station_efficiency_metrics(station_name)`
Rates station performance
```python
metrics = get_station_efficiency_metrics("Central Hub")
# Returns: {
#     avg_charging_time_minutes: 45.2,
#     total_sessions_30d: 240,
#     available_chargers: 5,
#     green_score: 8,
#     efficiency_rating: "Excellent",
#     recommendation: "Fast and eco-friendly!"
# }
```

### Analytics Dashboard
- Peak usage hours visualization
- 7-day demand forecast
- Price trend analysis
- Station efficiency rating
- Charging time statistics
- Eco-score tracking

---

## 3. Personalized Insights

### Location
- **Module:** `ai/insights.py`
- **Route:** `/user/insights`
- **Template:** `templates/user_insights.html`

### Functions

#### `get_user_charging_statistics(user_id)`
Overall charging summary
```python
stats = get_user_charging_statistics(user_id)
# Returns: {
#     total_sessions: 42,
#     total_units_charged: 450.5,
#     total_spent: 3604.00,
#     avg_per_session: 85.81,
#     favorite_station: "Downtown Hub",
#     favorite_count: 18
# }
```

#### `get_user_eco_impact(user_id)`
Environmental impact analysis
```python
eco = get_user_eco_impact(user_id)
# Returns: {
#     total_green_charges: 450.5,
#     avg_green_score: 7.8,
#     estimated_co2_emissions_kg: 90.1,
#     trees_equivalent: 4.5,
#     eco_rating: "Good Green Citizen",
#     recommendation: "Try to choose higher-rated green stations"
# }
```

#### `get_user_spending_insights(user_id)`
Spending patterns and optimization
```python
spending = get_user_spending_insights(user_id)
# Returns: {
#     spending_last_7_days: {total: 500.00, sessions: 6},
#     spending_last_30_days: {total: 1800.00, sessions: 24},
#     top_stations: [...],
#     cheapest_station: "Budget Charging",
#     recommendation: "Save money by charging at Budget Charging more often!"
# }
```

#### `get_personalized_recommendations(user_id)`
AI-generated recommendations
```python
recs = get_personalized_recommendations(user_id)
# Returns: [
#     {
#         type: "eco",
#         title: "Go Green",
#         message: "Switch to higher green-score stations...",
#         icon: "🌱"
#     },
#     ...
# ]
```

### Insights Dashboard Shows
- **Statistics:** Total sessions, units, spending
- **Spending Trends:** Last 7/14/30 days breakdown
- **Eco Impact:** CO₂ emissions, trees equivalent
- **Top Stations:** Most-used stations
- **Recommendations:** Personalized action items
- **Green Rating:** Eco-friendliness score

---

## 4. Natural Language Query System

### Location
- **Module:** `ai/nl_query.py`
- **Route:** `/user/nl-search`
- **Template:** `templates/nl_search.html`

### How It Works

#### `parse_natural_language_query(query)`
Converts natural text to structured search filters
```python
filters = parse_natural_language_query(
    "Find me a green station with fast charging within 10km"
)
# Returns: {
#     green_score_min: 7,
#     max_distance: 10,
#     fast_charging: True,
#     sort_by: "green_score",
#     intent: "greenest",
#     natural_explanation: "Looking for eco-friendly stations..."
# }
```

#### `search_with_natural_language(query, all_stations)`
End-to-end search
```python
results = search_with_natural_language(
    "Cheapest station near me",
    all_stations_list
)
# Returns: {
#     explanation: "Searching for affordable charging...",
#     results: [stations],
#     result_count: 5,
#     query_method: "ai"
# }
```

### Supported Query Types

| Intent | Example | Filters Applied |
|--------|---------|-----------------|
| **Greenest** | "Green station", "Eco-friendly" | green_score_min: 7, sort by green |
| **Cheapest** | "Budget", "Affordable", "Under 10₹" | sort by price, extract price |
| **Fastest** | "Fast charging", "Quick" | fast_charging: true |
| **Nearest** | "Near me", "Within 10km" | extract max_distance |
| **Balanced** | "Good station", "Reliable" | standard filtering |

### Query Examples
- "Green station with high eco score"
- "Cheapest charging within 5km"
- "Fast charging with multiple chargers"
- "Eco-friendly stations under ₹10/kWh"
- "Fast and cheap station near me"
- "Station with 4+ chargers"
- "Good green score and low price"

### Search Interface Features
- Natural text input
- Popular searches section
- Search tips & examples
- Result cards with actions
- Analytics link for each station

---

## File Structure

```
ai/
├── recommender.py      # Enhanced with Gemini
├── chatbot.py         # NEW: AI Chat
├── analytics.py       # NEW: Predictive Analytics
├── insights.py        # NEW: Personalized Insights
└── nl_query.py        # NEW: Natural Language Parser

templates/
├── user_dashboard.html          # UPDATED: New menu items
├── chat_interface.html          # NEW: Chat UI
├── user_insights.html           # NEW: Insights Dashboard
├── nl_search.html               # NEW: Natural Language Search
└── station_analytics.html       # NEW: Station Analytics

routes/
└── station_routes.py            # UPDATED: New endpoints
```

---

## Database Queries

### Analytics Data
- Uses `charging_sessions` table for historical analysis
- Groups by hour, weekday, date for predictions
- Calculates averages, trends, patterns
- No data modification - read-only analytics

### User Data
- Aggregates user's charging history
- Calculates spending patterns
- Analyzes eco-impact
- Generates recommendations

---

## Configuration

### Environment
Ensure `GEMINI_API_KEY` is set:
```powershell
$env:GEMINI_API_KEY="AIzaSyDTML0wuZQe9yDufXQJgZ-zrauIWcSj1lQ"
```

### Dependencies
```txt
google-generativeai>=0.3.0
```

---

## API Integration

### Gemini Pro Model
- **Model:** `gemini-pro`
- **Use Cases:** 
  - Chatbot responses
  - NL query parsing
  - Recommendation generation
  - Explanation generation

### Temperature Settings
- Chatbot: 0.7 (balanced creativity)
- NL Query Parser: 0.3 (deterministic)
- Recommendations: 0.7 (helpful but consistent)

### Rate Limiting
- Implement caching for common queries
- Batch requests where possible
- Monitor API usage on Google AI Studio

---

## Testing

### Chatbot
```
1. Go to /user/chat
2. Ask: "What stations have fast charging?"
3. Should get AI-powered response
```

### Analytics
```
1. Go to station list
2. Click "View Analytics" on a station
3. Should see peak hours, forecasts, price trends
```

### Insights
```
1. Go to /user/insights
2. Should see personalized recommendations
3. Check spending trends and eco-impact
```

### Natural Language Search
```
1. Go to /user/nl-search
2. Enter: "Green station within 10km"
3. Should filter stations by intent
```

---

## Future Enhancements

1. **Conversation Caching** - Save chat history per user
2. **Advanced NL Parsing** - Support more complex queries
3. **Real-time Updates** - Live peak hours, demand
4. **Recommendation Ranking** - ML-based station scoring
5. **Multi-language Support** - Spanish, Hindi, etc.
6. **Voice Input** - Speech-to-text queries
7. **Integration with Maps** - Show stations on map
8. **Alerts** - Notify users of price drops, peak times

---

## Troubleshooting

### "API returned error"
- Check API key is valid
- Verify internet connection
- Check API quota on Google AI Studio

### Slow responses
- Gemini API takes 2-3 seconds
- Consider caching results
- Implement request timeout

### Predictions inaccurate
- Not enough historical data
- Use fallback for new stations
- More data = better predictions

---

## Support

For issues or questions:
1. Check logs in terminal
2. Verify environment variables
3. Test with example queries
4. Contact support team

