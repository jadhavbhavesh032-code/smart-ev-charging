# 🚀 Deployment Checklist - Google Maps Integration

## Pre-Deployment Tasks

### ✅ Phase 1: API Configuration (30 min)

- [ ] **Google Maps API**
  - [ ] Create Google Cloud project
  - [ ] Enable Maps JavaScript API
  - [ ] Create API Key
  - [ ] Set HTTP referrer restrictions
  - [ ] Document API key securely
  - [ ] Set environment variable: `GOOGLE_MAPS_API_KEY`

- [ ] **Google Gemini API** (if not already done)
  - [ ] Create API key at console.ai.google.com
  - [ ] Set environment variable: `GEMINI_API_KEY`

- [ ] **Environment Variables**
  - [ ] Windows: Use `$env:` in PowerShell
  - [ ] Linux/Mac: Use `export` command
  - [ ] Or create `.env` file with both keys
  - [ ] Verify: `python app.py` starts without errors

### ✅ Phase 2: Code Verification (15 min)

- [ ] **File Structure**
  - [ ] `templates/map_search.html` exists
  - [ ] `templates/map_booking.html` exists
  - [ ] `ai/map_utils.py` exists
  - [ ] Route updates in `routes/station_routes.py`
  - [ ] Dashboard updated with map menu item

- [ ] **Python Tests**
  ```bash
  python -c "from ai.map_utils import *; print('✅ Imports OK')"
  python verify_all.py  # Run full verification
  ```

- [ ] **Database**
  - [ ] Database initialized: `python verify_db.py`
  - [ ] At least 2 test stations in database
  - [ ] Stations have `approved=1` status
  - [ ] No schema errors

### ✅ Phase 3: Local Testing (45 min)

**Start Application**
```bash
$env:GOOGLE_MAPS_API_KEY = "YOUR_KEY"
$env:GEMINI_API_KEY = "YOUR_KEY"
python app.py
# Visit http://localhost:5000
```

**Test Registration & Login**
- [ ] Register new user account
- [ ] Login successfully
- [ ] Session persists
- [ ] Logout works

**Test Maps Feature**
- [ ] Navigate to Dashboard
- [ ] Click "Google Maps Search" menu item
- [ ] Map loads and displays stations
- [ ] See station markers on map
- [ ] Markers are color-coded (green/yellow/orange/red)

**Test All Search Modes**
- [ ] **All Stations**: Select "All Stations" radio button
  - [ ] All stations appear on map
  - [ ] Results list shows all stations
  - [ ] Click marker shows info window
  - [ ] Distance not shown (N/A for all search)

- [ ] **Nearby Search**: Select "Nearby" radio button
  - [ ] Enter radius (e.g., 10 km)
  - [ ] Click "Use My Location"
  - [ ] Browser requests geolocation permission
  - [ ] Click "Allow" or "Permit"
  - [ ] Map updates with nearby stations only
  - [ ] Distance shown in results

- [ ] **Filter Search**: Select "Filter" radio button
  - [ ] Set Green Score: 6+ (Good)
  - [ ] Set Max Price: ₹12/kWh
  - [ ] Set Min Chargers: 2
  - [ ] Click "Search"
  - [ ] Results show only matching stations

**Test Booking Flow**
- [ ] Click "Book" on any station
- [ ] Booking page loads correctly
- [ ] Station details displayed
- [ ] Price calculator works:
  - [ ] Default: 10 kWh
  - [ ] Click +/- buttons to adjust
  - [ ] Price updates in real-time
- [ ] Quick select buttons work (20/40/60/80 kWh)
- [ ] Service fee calculated (5%)
- [ ] Total price shows correctly
- [ ] CO₂ savings display
- [ ] Accept terms checkbox works
- [ ] Confirm button redirects to `/user/charge`
- [ ] Check units parameter in URL: `?units=40`

**Test Responsive Design**
- [ ] Desktop (1920x1080): All elements visible
- [ ] Tablet (768x1024): Layout adjusts correctly
- [ ] Mobile (375x667): 
  - [ ] Map is readable
  - [ ] Buttons are tappable
  - [ ] Results list scrollable
  - [ ] Navigation works

**Test Error Handling**
- [ ] Invalid API key: Shows error message
- [ ] No geolocation permission: Graceful fallback
- [ ] Invalid radius: Reset to default
- [ ] No stations in database: Show helpful message
- [ ] Network timeout: Retry or error message

### ✅ Phase 4: Browser Testing (20 min)

Test on each supported browser:

- [ ] **Chrome 90+**
  - [ ] Map loads
  - [ ] All features work
  - [ ] No console errors

- [ ] **Firefox 88+**
  - [ ] Map loads
  - [ ] Geolocation works
  - [ ] Responsive design ok

- [ ] **Safari 14+**
  - [ ] Map loads
  - [ ] Geolocation works
  - [ ] Price calculation correct

- [ ] **Edge 90+**
  - [ ] All features work
  - [ ] No performance issues

### ✅ Phase 5: Performance Testing (15 min)

**Load Time Tests**
- [ ] Initial page load: <3 seconds
- [ ] Map render: <2 seconds
- [ ] Search response: <500ms
- [ ] Booking page load: <1 second

**Stress Tests**
- [ ] Open map 5 times rapidly: No crashes
- [ ] Search 10 times consecutively: Consistent results
- [ ] Rapid zoom in/out on map: No lag
- [ ] Multiple info windows: Opening and closing smooth

**Database Tests**
- [ ] 50 stations loaded: Performance acceptable
- [ ] 100 stations loaded: Performance acceptable
- [ ] Multiple concurrent searches: No locking

### ✅ Phase 6: Security Review (20 min)

- [ ] **API Keys**
  - [ ] No hardcoded keys in code
  - [ ] Keys in environment variables only
  - [ ] Never logged or printed
  - [ ] HTTP referrer restrictions set
  - [ ] API usage monitored

- [ ] **Authentication**
  - [ ] Routes require valid session
  - [ ] Redirect to login if not authenticated
  - [ ] Role check: role == "user"
  - [ ] Admin cannot access user routes

- [ ] **Input Validation**
  - [ ] Invalid radius rejected
  - [ ] Negative values rejected
  - [ ] SQL injection tests pass
  - [ ] XSS protection active

- [ ] **Data Privacy**
  - [ ] Location data not logged
  - [ ] User IPs not tracked
  - [ ] Session data encrypted
  - [ ] No sensitive data in URLs

### ✅ Phase 7: Documentation Review (10 min)

- [ ] **All docs present**
  - [ ] `GOOGLE_MAPS_FEATURE_GUIDE.md`
  - [ ] `GOOGLE_MAPS_SETUP.md`
  - [ ] `GOOGLE_MAPS_IMPLEMENTATION.md`
  - [ ] `DOCUMENTATION_INDEX.md`
  - [ ] `GOOGLE_MAPS_QUICKSTART.py`

- [ ] **Docs are accurate**
  - [ ] API key setup steps verified
  - [ ] Environment variable examples correct
  - [ ] File paths match actual files
  - [ ] URLs are valid

- [ ] **Docs are complete**
  - [ ] Troubleshooting section filled
  - [ ] Examples provided
  - [ ] Performance tips included
  - [ ] Security guidelines present

---

## Production Deployment

### ✅ Phase 8: Server Setup (1 hour)

**Server Configuration**
- [ ] Operating System: Windows Server 2019+ or Linux
- [ ] Python: 3.9+ installed
- [ ] Dependencies: `pip install -r requirements.txt`
- [ ] Firewall: Port 5000 or 80/443 if proxied
- [ ] SSL Certificate: Valid HTTPS certificate
- [ ] Domain: DNS configured

**Database**
- [ ] Production database instance
- [ ] Regular backups scheduled
- [ ] Monitoring enabled
- [ ] Growth strategy planned

**Environment**
- [ ] API keys configured on server
- [ ] Not in version control
- [ ] Secured with proper permissions
- [ ] Monitored for leaks

### ✅ Phase 9: Deployment

**Deploy Code**
```bash
# On production server
git clone <repo>
cd smart-ev-charging
pip install -r requirements.txt
python app.py --host 0.0.0.0 --port 5000
```

Or with gunicorn (recommended):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Verify Production**
- [ ] Application starts without errors
- [ ] No error messages in logs
- [ ] Maps feature accessible
- [ ] Database connection working
- [ ] APIs responding correctly

### ✅ Phase 10: Monitoring (ongoing)

**Set Up Monitoring**
- [ ] Error logging service (e.g., Sentry)
- [ ] Performance monitoring
- [ ] API quota monitoring
- [ ] Database performance
- [ ] Server uptime monitoring

**Alerts**
- [ ] API key quota exceeded
- [ ] Database connection failed
- [ ] Server down notifications
- [ ] High error rate alerts
- [ ] Performance degradation alerts

---

## Post-Deployment Tasks

### ✅ User Communication

- [ ] Notify users of new feature
- [ ] Send tutorial/guide
- [ ] Collect initial feedback
- [ ] Monitor bug reports
- [ ] Track feature usage

### ✅ Analytics Setup

- [ ] Track map searches
- [ ] Track bookings from map
- [ ] Track conversion rates
- [ ] Monitor popular stations
- [ ] Analyze user patterns

### ✅ Optimization

- [ ] Review performance data
- [ ] Optimize slow queries
- [ ] Cache frequently accessed data
- [ ] Consider CDN for static assets
- [ ] Plan scaling strategy

---

## Rollback Plan

If issues occur in production:

1. **Minor Issues** (cosmetic, non-critical)
   - [ ] Create patch
   - [ ] Deploy fix
   - [ ] No rollback needed

2. **Moderate Issues** (feature broken)
   - [ ] Deploy hotfix
   - [ ] Or disable feature temporarily
   - [ ] Post notice to users
   - [ ] Rollback if hotfix fails

3. **Critical Issues** (data loss, security)
   - [ ] Immediately rollback to previous version
   - [ ] Investigate root cause
   - [ ] Restart map feature after fix
   - [ ] Notify affected users

**Rollback Command**
```bash
# Stop current version
# Restore previous database backup
# Redeploy previous code
# Verify functionality
git revert <commit_hash>
python app.py
```

---

## Final Checklist

Before going live:

- [ ] All tests passed ✅
- [ ] Documentation complete ✅
- [ ] Security review passed ✅
- [ ] Performance acceptable ✅
- [ ] Monitoring configured ✅
- [ ] Backup strategy set ✅
- [ ] Team trained ✅
- [ ] User documentation ready ✅
- [ ] Support plan established ✅
- [ ] Analytics tracking ✅

---

## Success Metrics

After deployment, track:

| Metric | Target | Period |
|--------|--------|--------|
| Feature Adoption | 30% of users | 1 month |
| Booking Conversion | 15% from map | 1 month |
| User Satisfaction | 4.5/5 rating | 2 weeks |
| System Uptime | 99.9% | 1 month |
| Error Rate | <0.1% | ongoing |
| Avg Page Load | <2s | ongoing |

---

## Sign-Off

- [ ] **Developer**: Code ready for production
- [ ] **QA**: All tests passed
- [ ] **Security**: Security review completed
- [ ] **DevOps**: Deployment plan approved
- [ ] **Product Manager**: Feature approved
- [ ] **Leadership**: Go-live approved

---

**Deployment Status**: ⏳ Ready for Deployment
**Next Step**: Begin Phase 1 (API Configuration)
**Expected Go-Live**: [DATE]

---

For questions, see [GOOGLE_MAPS_SETUP.md](GOOGLE_MAPS_SETUP.md) or [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
