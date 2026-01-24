# Smart EV Charging Platform - Project Documentation

## Team Details
- **Team Name:** Smart EV Charging Team
- **Team Members:**
  - Sachin Jha
  - Prince Jha
  - Bhavesh Jadhav

---

## Domain of Your Project
**Electric Vehicle (EV) Charging Infrastructure & Services** - A comprehensive platform for discovering, booking, and managing EV charging stations with AI-powered features for enhanced user experience.

---

## Idea

### Problem Statement
The electric vehicle adoption is rapidly increasing, but users face significant challenges:
- **Lack of Visibility**: No unified platform to discover available charging stations
- **Inefficient Planning**: Users cannot predict peak hours or plan cost-effective charging
- **Poor User Experience**: Complex interfaces for finding and booking stations
- **Limited Insights**: Users don't understand their charging patterns or environmental impact
- **Communication Gap**: No easy way to get support for charging-related queries

### Solution
**Smart EV Charging Platform** - An intelligent, all-in-one web application that provides:

1. **Interactive Station Discovery** - Google Maps integration with color-coded stations based on availability, pricing, and eco-friendliness
2. **AI-Powered Chatbot** - 24/7 support for station queries, pricing information, and troubleshooting
3. **Predictive Analytics** - Real-time forecasts of station demand, peak hours, and price trends
4. **Personalized Insights** - Comprehensive dashboard showing user charging habits, spending trends, and environmental impact
5. **Natural Language Search** - Find stations by describing needs in natural language (e.g., "cheap and fast stations nearby")
6. **Multi-User Platform** - Support for Users, Station Owners, and Administrators with role-based dashboards

---

## Tech Stack Used

### Backend
- **Flask 2.3.2** - Python web framework for backend API and routing
- **SQLite** - Lightweight database for storing users, stations, and charging sessions
- **Python 3.8+** - Core programming language

### AI/ML Services
- **Google Generative AI (Gemini)** - Powers chatbot, analytics, insights, and NL search features
- **Natural Language Processing** - For intelligent query understanding and responses

### Frontend
- **HTML5/CSS3** - Responsive web templates
- **JavaScript** - Interactive features and dynamic UI
- **Bootstrap/Tailwind CSS** - Responsive design framework
- **Google Maps JavaScript API** - Interactive mapping and geolocation services

### Additional Technologies
- **python-dotenv** - Environment variable management for API keys
- **Session Management** - Flask sessions for user authentication
- **Geolocation API** - Browser geolocation for finding nearby stations
- **Haversine Formula** - Distance calculation between coordinates

---

## How to Execute Your Code

### Prerequisites
- Python 3.8 or higher installed
- Google Cloud API Keys:
  - Google Maps JavaScript API Key
  - Google Generative AI (Gemini) API Key
- pip package manager
- Web browser (Chrome, Firefox, Edge, Safari)
- Windows/Mac/Linux operating system

### Step-by-Step Setup Instructions

#### 1. **Clone/Download the Project**
```bash
# Navigate to project directory
cd "Smart EV Charging"
```

#### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

**Required Packages:**
- Flask==2.3.2
- google-generativeai>=0.3.0
- python-dotenv>=1.0.0

#### 3. **Set Up Environment Variables**

Create a `.env` file in the project root directory with the following:

```
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
GEMINI_API_KEY=your_google_gemini_api_key_here
```

**Getting API Keys:**

**Google Maps API Key:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "Maps JavaScript API"
4. Go to Credentials → Create API Key
5. Restrict to HTTP referrers (optional but recommended)
6. Copy the key to your `.env` file

**Google Gemini API Key:**
1. Go to [Google AI Studio](https://console.ai.google.com/)
2. Click "Create API Key"
3. Copy the key to your `.env` file

#### 4. **Initialize the Database** (First Time Only)
```bash
python verify_db.py
```

This will:
- Create SQLite database
- Initialize all tables (users, stations, charging_sessions, admin)
- Create a default admin account (username: `admin`, password: `admin123`)

#### 5. **Seed Demo Data** (Optional - For Testing)
```bash
python seed_demo_data.py
```

This populates the database with sample stations and test data.

#### 6. **Run the Application**

**On Windows (PowerShell):**
```powershell
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
python app.py
```

**On Mac/Linux:**
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
python app.py
```

#### 7. **Access the Application**
Open your web browser and navigate to:
```
http://localhost:5000
```

### Default Login Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`
- Access: http://localhost:5000/admin/login

**Demo User Accounts:** (After running seed_demo_data.py)
- Create new accounts via registration at http://localhost:5000/register

---

## Features Overview

### 🏠 Home Page
- Welcome screen with platform overview
- Quick navigation to login/register
- Feature highlights

### 👤 User Dashboard
- View charging session history
- Track statistics (total sessions, units charged, green score)
- Quick access to all user features
- Menu items for:
  - Google Maps Search
  - AI Chat Assistant
  - Station Analytics
  - Personal Insights
  - Natural Language Search

### 🗺️ Google Maps Search
**Path:** `/user/map-search`
- Interactive map with color-coded station markers
- Three search modes:
  1. **All Stations** - Browse all available stations
  2. **Nearby** - Find stations within specified radius using geolocation
  3. **Filter** - Search by green score, price, and charger count
- One-click booking from map
- Real-time distance calculation

### 🤖 AI Chat Assistant
**Path:** `/user/chat`
- 24/7 AI chatbot for customer support
- Answers questions about:
  - Charging station locations and features
  - Pricing information
  - Troubleshooting
  - Eco-friendly options
  - Booking assistance
- Example query buttons for quick help
- Natural conversation interface

### 📊 Predictive Analytics
**Path:** `/user/station-analytics/<station_name>`
- Peak usage hour analysis with intensity levels
- 7-day demand forecast with confidence scores
- 30-day price trend analysis
- Station efficiency ratings
- Historical activity tracking
- Visual charts and heatmaps

### 👁️ Personal Insights
**Path:** `/user/insights`
- Charging statistics and habits
- Spending analysis (7/14/30 days)
- Environmental impact metrics (CO₂ saved, equivalent trees)
- Favorite stations ranking
- AI-powered recommendations
- Eco-rating and green score

### 🔍 Natural Language Search
**Path:** `/user/nl-search`
- Search for stations using natural text
- Automatic intent parsing:
  - "cheap" → low price filter
  - "fast" → high charger capacity
  - "green/eco" → high green score
  - "near" → nearby location filter
- Intelligent result ranking
- Example searches provided

### 👨‍💼 Station Owner Dashboard
**Path:** `/owner/dashboard`
- Manage owned charging stations
- View revenue and user statistics
- Monitor station performance
- Add and edit stations
- View active charging sessions

### 🛡️ Admin Dashboard
**Path:** `/admin/dashboard`
- Monitor all platform activity
- User management
- Station approval and verification
- Revenue tracking
- System statistics
- User and station editing capabilities

---

## Code Sample

### Running the Application

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API keys in .env file
# GOOGLE_MAPS_API_KEY=your_key
# GEMINI_API_KEY=your_key

# 3. Initialize database
python verify_db.py

# 4. Seed demo data (optional)
python seed_demo_data.py

# 5. Run the Flask app
python app.py

# 6. Open browser
# http://localhost:5000
```

### Example: Creating a Charging Session
```python
# From routes/user_routes.py
from models.db import get_db

def book_charging_session(station_name, units, user_id):
    conn = get_db()
    cur = conn.cursor()
    
    # Calculate cost
    price_per_unit = get_station_price(station_name)
    amount = units * price_per_unit
    
    # Create session
    cur.execute("""
        INSERT INTO charging_sessions 
        (user_id, station_name, units, amount, status)
        VALUES (?, ?, ?, ?, 'Pending')
    """, (user_id, station_name, units, amount))
    
    conn.commit()
    conn.close()
    return True
```

### Example: AI Chat Query
```python
# From ai/chatbot.py
import google.generativeai as genai

def get_chatbot_response(user_query, context):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    You are a helpful EV Charging Station Assistant.
    Context: {context}
    User Query: {user_query}
    """
    
    response = model.generate_content(prompt)
    return response.text
```

---

## Project Links & Resources

### GitHub Repository
[GitHub Link - To be added when repository is published]

### Deployment
- **Local:** http://localhost:5000
- **Production:** [To be deployed]

### API Keys Required
- Google Maps API: [https://console.cloud.google.com/](https://console.cloud.google.com/)
- Gemini AI API: [https://console.ai.google.com/](https://console.ai.google.com/)

### Documentation Files
- `FEATURES_OVERVIEW.md` - Detailed feature descriptions
- `DEPLOYMENT_CHECKLIST.md` - Production deployment guide
- `GOOGLE_MAPS_FEATURE_GUIDE.md` - Maps feature documentation
- `GEMINI_SETUP_COMPLETE.md` - AI setup instructions

---

## Key Project Statistics

- **Total Python Files:** 20+
- **HTML Templates:** 18
- **AI Features:** 4 (Chatbot, Analytics, Insights, NL Search)
- **User Roles:** 3 (User, Owner, Admin)
- **Database Tables:** 5 (Users, Stations, Sessions, Admin, Queue)
- **API Integrations:** 2 (Google Maps, Google Gemini)
- **Lines of Code:** 3000+

---

## Troubleshooting

### Common Issues & Solutions

**Issue:** "ModuleNotFoundError: No module named 'flask'"
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue:** "Google Maps API key not valid"
- Verify API key in `.env` file
- Ensure Maps JavaScript API is enabled in Google Cloud Console
- Check API key restrictions

**Issue:** "GEMINI_API_KEY environment variable not found"
- Create `.env` file with your API key
- Restart the Flask application
- Or set environment variable: `$env:GEMINI_API_KEY = "your_key"`

**Issue:** "Database is locked"
- Close any open database connections
- Restart the Flask application
- Check no other instances are running

---

## Future Enhancements

1. **Payment Integration** - Real payment processing with multiple gateways
2. **Mobile App** - Native iOS/Android applications
3. **Real-time Notifications** - Push notifications for users and owners
4. **Advanced Reporting** - Export analytics to PDF/Excel
5. **Machine Learning** - Demand prediction model
6. **Rating System** - User reviews for stations
7. **Loyalty Program** - Rewards for frequent users
8. **EV Compatibility** - Filter stations by vehicle type
9. **Energy Source** - Filter by renewable energy sources
10. **API Documentation** - RESTful API for third-party integrations

---

## Contact & Support

For questions or support, please reach out to the team:
- Sachin Jha
- Prince Jha
- Bhavesh Jadhav

---

**Last Updated:** January 24, 2026
**Version:** 1.0 - Release Candidate
