"""
Multi-tier caching system for product data
Tier 1: In-memory cache (Redis) - Fastest access
Tier 2: Local database cache (SQLite) - Persistent storage
Tier 3: File-based cache - Backup storage
"""

import redis
import sqlite3
import json
import pickle
import hashlib
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import os
from pathlib import Path

class CacheManager:
    def __init__(self, 
                 redis_url: str = "redis://localhost:6379",
                 db_path: str = "cache.db",
                 file_cache_dir: str = "file_cache"):
        self.redis_client = None
        self.db_path = db_path
        self.file_cache_dir = Path(file_cache_dir)
        self.file_cache_dir.mkdir(exist_ok=True)
        
        # Initialize Redis (Tier 1)
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            self.redis_client.ping()
            print("✅ Redis cache connected")
        except Exception as e:
            print(f"⚠️ Redis not available: {e}")
            self.redis_client = None
        
        # Initialize SQLite (Tier 2)
        self._init_sqlite()
        
        # Cache TTL settings (in seconds)
        self.cache_ttl = {
            'product_details': 3600,      # 1 hour
            'search_results': 1800,       # 30 minutes
            'category_data': 7200,        # 2 hours
            'product_reviews': 14400,     # 4 hours
            'trending_products': 900,     # 15 minutes
        }
    
    def _init_sqlite(self):
        """Initialize SQLite database for persistent caching"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cache_data (
                key TEXT PRIMARY KEY,
                data TEXT,
                cache_type TEXT,
                created_at TIMESTAMP,
                expires_at TIMESTAMP
            )
        ''')
        
        # Create index for faster lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_cache_expires 
            ON cache_data(cache_type, expires_at)
        ''')
        
        conn.commit()
        conn.close()
        print("✅ SQLite cache initialized")
    
    def _generate_cache_key(self, data_type: str, identifier: str) -> str:
        """Generate consistent cache key"""
        key_string = f"{data_type}:{identifier}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, data_type: str, identifier: str) -> Optional[Dict]:
        """Get data from cache (tries all tiers)"""
        cache_key = self._generate_cache_key(data_type, identifier)
        
        # Tier 1: Try Redis first
        if self.redis_client:
            try:
                cached_data = self.redis_client.get(cache_key)
                if cached_data:
                    print(f"🚀 Cache HIT (Redis): {data_type}:{identifier}")
                    return json.loads(cached_data)
            except Exception as e:
                print(f"Redis get error: {e}")
        
        # Tier 2: Try SQLite
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT data FROM cache_data 
                WHERE key = ? AND expires_at > ?
            ''', (cache_key, datetime.now()))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                data = json.loads(result[0])
                print(f"💾 Cache HIT (SQLite): {data_type}:{identifier}")
                
                # Promote to Redis if available
                if self.redis_client:
                    try:
                        self.redis_client.setex(
                            cache_key, 
                            self.cache_ttl.get(data_type, 3600),
                            json.dumps(data)
                        )
                    except Exception:
                        pass
                
                return data
        except Exception as e:
            print(f"SQLite get error: {e}")
        
        # Tier 3: Try file cache
        try:
            file_path = self.file_cache_dir / f"{cache_key}.json"
            if file_path.exists():
                with open(file_path, 'r') as f:
                    cache_entry = json.load(f)
                
                # Check if not expired
                if datetime.fromisoformat(cache_entry['expires_at']) > datetime.now():
                    data = cache_entry['data']
                    print(f"📁 Cache HIT (File): {data_type}:{identifier}")
                    
                    # Promote to higher tiers
                    self._promote_to_higher_tiers(cache_key, data, data_type)
                    return data
        except Exception as e:
            print(f"File cache get error: {e}")
        
        print(f"❌ Cache MISS: {data_type}:{identifier}")
        return None
    
    def set(self, data_type: str, identifier: str, data: Dict) -> bool:
        """Set data in all cache tiers"""
        cache_key = self._generate_cache_key(data_type, identifier)
        ttl = self.cache_ttl.get(data_type, 3600)
        expires_at = datetime.now() + timedelta(seconds=ttl)
        
        success = True
        
        # Tier 1: Redis
        if self.redis_client:
            try:
                self.redis_client.setex(cache_key, ttl, json.dumps(data))
                print(f"✅ Cached to Redis: {data_type}:{identifier}")
            except Exception as e:
                print(f"Redis set error: {e}")
                success = False
        
        # Tier 2: SQLite
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO cache_data 
                (key, data, cache_type, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (cache_key, json.dumps(data), data_type, datetime.now(), expires_at))
            
            conn.commit()
            conn.close()
            print(f"✅ Cached to SQLite: {data_type}:{identifier}")
        except Exception as e:
            print(f"SQLite set error: {e}")
            success = False
        
        # Tier 3: File cache
        try:
            cache_entry = {
                'data': data,
                'created_at': datetime.now().isoformat(),
                'expires_at': expires_at.isoformat()
            }
            
            file_path = self.file_cache_dir / f"{cache_key}.json"
            with open(file_path, 'w') as f:
                json.dump(cache_entry, f)
            print(f"✅ Cached to File: {data_type}:{identifier}")
        except Exception as e:
            print(f"File cache set error: {e}")
            success = False
        
        return success
    
    def _promote_to_higher_tiers(self, cache_key: str, data: Dict, data_type: str):
        """Promote cache data to higher tiers for faster access"""
        ttl = self.cache_ttl.get(data_type, 3600)
        
        # Promote to SQLite if not there
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM cache_data WHERE key = ?', (cache_key,))
            if not cursor.fetchone():
                expires_at = datetime.now() + timedelta(seconds=ttl)
                cursor.execute('''
                    INSERT INTO cache_data 
                    (key, data, cache_type, created_at, expires_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (cache_key, json.dumps(data), data_type, datetime.now(), expires_at))
                conn.commit()
            conn.close()
        except Exception:
            pass
        
        # Promote to Redis
        if self.redis_client:
            try:
                self.redis_client.setex(cache_key, ttl, json.dumps(data))
            except Exception:
                pass
    
    def invalidate(self, data_type: str, identifier: str = None) -> bool:
        """Invalidate cache entries"""
        if identifier:
            # Invalidate specific item
            cache_key = self._generate_cache_key(data_type, identifier)
            return self._invalidate_key(cache_key)
        else:
            # Invalidate all items of type
            return self._invalidate_type(data_type)
    
    def _invalidate_key(self, cache_key: str) -> bool:
        """Invalidate specific cache key from all tiers"""
        success = True
        
        # Redis
        if self.redis_client:
            try:
                self.redis_client.delete(cache_key)
            except Exception:
                success = False
        
        # SQLite
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM cache_data WHERE key = ?', (cache_key,))
            conn.commit()
            conn.close()
        except Exception:
            success = False
        
        # File cache
        try:
            file_path = self.file_cache_dir / f"{cache_key}.json"
            if file_path.exists():
                file_path.unlink()
        except Exception:
            success = False
        
        return success
    
    def _invalidate_type(self, data_type: str) -> bool:
        """Invalidate all cache entries of a specific type"""
        success = True
        
        # SQLite - get all keys of this type
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT key FROM cache_data WHERE cache_type = ?', (data_type,))
            keys = [row[0] for row in cursor.fetchall()]
            
            # Delete from SQLite
            cursor.execute('DELETE FROM cache_data WHERE cache_type = ?', (data_type,))
            conn.commit()
            conn.close()
            
            # Delete from Redis and file cache
            for key in keys:
                if self.redis_client:
                    try:
                        self.redis_client.delete(key)
                    except Exception:
                        pass
                
                try:
                    file_path = self.file_cache_dir / f"{key}.json"
                    if file_path.exists():
                        file_path.unlink()
                except Exception:
                    pass
        except Exception:
            success = False
        
        return success
    
    def cleanup_expired(self) -> int:
        """Clean up expired cache entries"""
        removed_count = 0
        
        # SQLite cleanup
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT key FROM cache_data WHERE expires_at < ?', (datetime.now(),))
            expired_keys = [row[0] for row in cursor.fetchall()]
            
            cursor.execute('DELETE FROM cache_data WHERE expires_at < ?', (datetime.now(),))
            removed_count += cursor.rowcount
            conn.commit()
            conn.close()
            
            # File cache cleanup
            for key in expired_keys:
                try:
                    file_path = self.file_cache_dir / f"{key}.json"
                    if file_path.exists():
                        file_path.unlink()
                except Exception:
                    pass
        except Exception as e:
            print(f"Cleanup error: {e}")
        
        if removed_count > 0:
            print(f"🧹 Cleaned up {removed_count} expired cache entries")
        
        return removed_count
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        stats = {
            'redis_available': self.redis_client is not None,
            'sqlite_entries': 0,
            'file_cache_entries': 0
        }
        
        # SQLite stats
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM cache_data WHERE expires_at > ?', (datetime.now(),))
            stats['sqlite_entries'] = cursor.fetchone()[0]
            conn.close()
        except Exception:
            pass
        
        # File cache stats
        try:
            stats['file_cache_entries'] = len(list(self.file_cache_dir.glob('*.json')))
        except Exception:
            pass
        
        return stats