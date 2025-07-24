# 🚀 Live Data Integration Setup Guide

This guide will help you set up Curi with live Best Buy data and intelligent caching to avoid rate limits.

## 🎯 Overview

Your new system includes:
- **3-Tier Caching**: Redis (fast) → SQLite (persistent) → File (backup)
- **Smart Rate Limiting**: Respects Best Buy's 5 req/sec limit
- **Multiple Data Sources**: Best Buy API + RapidAPI fallbacks
- **Intelligent Prefetching**: Pre-loads popular categories
- **Performance Monitoring**: Real-time cache hit rates and API usage

## 🛠️ Quick Setup (5 minutes)

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Verify Environment Variables
Your root `.env` file already has the Best Buy API key configured. If you want to add optional services:

```bash
# Edit the root .env file to add optional keys
nano .env
```

Optional additions:
```env
RAPIDAPI_KEY=your_rapidapi_key_here  # For fallback data sources
REDIS_URL=redis://localhost:6379     # For faster caching
```

### 3. Install Redis (Optional but Recommended)
```bash
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis-server

# Windows
# Download from https://redis.io/download
```

### 4. Start the Backend
```bash
python main.py
```

You should see:
```
🔄 Initializing Curi backend with live data...
🌐 Using live Best Buy API data
📦 Pre-fetching popular product categories...
✅ laptop: 100 products
✅ phone: 100 products
...
🚀 Curi backend ready!
```

## 📊 System Architecture

### Cache Strategy
```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Redis     │    │   SQLite     │    │ File Cache  │
│ (In-Memory) │────│ (Persistent) │────│  (Backup)   │
│  < 1ms      │    │   ~5ms       │    │   ~50ms     │
└─────────────┘    └──────────────┘    └─────────────┘
       ↑                    ↑                   ↑
   Hot data           Warm data          Cold backup
```

### Rate Limiting
- **Best Buy API**: 4 requests/second (conservative)
- **Burst Capacity**: 10 requests/minute for peaks
- **Automatic Backoff**: Waits if rate limited
- **Smart Queuing**: Prioritizes user searches

### Data Flow
```
User Query → Cache Check → API Call (if miss) → Cache Store → Response
     ↓
Cache Hit: ~1ms response
Cache Miss: ~200ms (API + processing)
```

## 🎮 Testing Your Setup

### Test 1: Basic Search
```bash
curl "http://localhost:8000/products/search?query=laptop&limit=5"
```

### Test 2: Cache Performance
```bash
curl "http://localhost:8000/admin/cache/stats"
```

Expected response:
```json
{
  "cache_stats": {
    "bestbuy_calls": 10,
    "rapidapi_calls": 0,
    "cache_hits": 45,
    "total_requests": 55,
    "cache_hit_rate": 0.82,
    "redis_available": true,
    "sqlite_entries": 500
  }
}
```

### Test 3: System Status
```bash
curl "http://localhost:8000/admin/system/status"
```

## 🔧 Advanced Configuration

### Rate Limit Tuning
Edit `data_sources.py`:
```python
# Conservative (recommended for production)
self.rate_limiter = RateLimiter(max_requests=4, time_window=1)

# Aggressive (if you have higher limits)
self.rate_limiter = RateLimiter(max_requests=5, time_window=1)
```

### Cache TTL Settings
Edit `.env`:
```env
CACHE_TTL_PRODUCTS=3600    # Product details: 1 hour
CACHE_TTL_SEARCH=1800      # Search results: 30 minutes
CACHE_TTL_REVIEWS=14400    # Reviews: 4 hours
```

### Prefetch Categories
Edit `live_data_processor.py`:
```python
self.popular_queries = [
    "laptop", "phone", "headphones", "tablet", "smartwatch",
    "gaming", "camera", "speaker", "tv", "fitness tracker",
    # Add your popular categories here
]
```

## 🚨 Troubleshooting

### Issue: Rate Limited (429 Error)
**Solution**: The system handles this automatically, but you can:
1. Reduce rate limits in `data_sources.py`
2. Increase cache TTL values
3. Check if Redis is running for better caching

### Issue: No Products Found
**Debugging**:
```bash
# Check system status
curl "http://localhost:8000/admin/system/status"

# Check cache stats
curl "http://localhost:8000/admin/cache/stats"

# Force cache refresh
curl -X POST "http://localhost:8000/admin/cache/refresh"
```

### Issue: Slow Response Times
**Solutions**:
1. **Install Redis**: Dramatically improves cache performance
2. **Warm up cache**: Run popular searches once
3. **Check network**: Best Buy API response times vary

### Issue: Cache Growing Too Large
**Solution**:
```bash
# Clean up expired entries
curl -X DELETE "http://localhost:8000/admin/cache/cleanup"
```

## 📈 Performance Optimization

### Pre-warming Cache
Run this script to warm up your cache:
```python
import asyncio
from live_data_processor import LiveDataProcessor

async def warm_cache():
    processor = LiveDataProcessor('your_api_key')
    
    # Popular searches to pre-cache
    searches = [
        "gaming laptop", "wireless headphones", "smartphone",
        "4k tv", "bluetooth speaker", "fitness tracker"
    ]
    
    for search in searches:
        await processor.search_products_live(search, 50)
        print(f"Cached: {search}")

asyncio.run(warm_cache())
```

### Monitoring
Add to your monitoring:
```bash
# Cache hit rate (aim for >80%)
curl "http://localhost:8000/admin/cache/stats" | jq '.cache_stats.cache_hit_rate'

# API calls per hour (monitor for rate limits)
curl "http://localhost:8000/admin/cache/stats" | jq '.cache_stats.bestbuy_calls'
```

## 🔄 Production Deployment

### Environment Variables
```env
# Production settings
NODE_ENV=production
REDIS_URL=redis://your-redis-server:6379
DATABASE_URL=postgresql://user:pass@host:5432/cache_db

# Higher performance settings
CACHE_TTL_PRODUCTS=7200     # 2 hours in production
BESTBUY_RATE_LIMIT=5        # Use full API limit

# Background refresh
DATA_REFRESH_INTERVAL_HOURS=4
```

### Background Tasks
Add to your deployment:
```python
# Scheduled cache refresh (every 4 hours)
@app.on_event("startup")
async def schedule_cache_refresh():
    async def refresh_task():
        while True:
            await asyncio.sleep(4 * 3600)  # 4 hours
            await data_processor.refresh_cache()
    
    asyncio.create_task(refresh_task())
```

## 🎉 Success Metrics

Your setup is working well if you see:
- **Cache Hit Rate**: >80%
- **Response Time**: <200ms for cached, <1s for API calls
- **API Calls**: <1000 per hour
- **Error Rate**: <1%

## 💡 Pro Tips

1. **Monitor your API usage**: Best Buy has daily limits too
2. **Use RapidAPI as backup**: Helps when Best Buy is down
3. **Cache popular searches**: Pre-load trending products
4. **Monitor cache size**: Clean up regularly in production
5. **Use Redis in production**: Much faster than file/SQLite only

## 📞 Support

If you encounter issues:
1. Check the logs for specific errors
2. Verify your API keys are correct
3. Test with a simple curl command first
4. Check Redis/SQLite connections

The system is designed to be resilient - it will fall back to cached data if APIs fail, ensuring your users always get results!