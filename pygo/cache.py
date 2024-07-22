import json
import os
import atexit
from hashlib import sha256

CACHE_DIR = 'cache'
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def hash_key(key):
    """Generate a SHA-256 hash of the key to use as a filename."""
    return sha256(key.encode()).hexdigest()

class Cache:
    @staticmethod
    def get(key):
        """Retrieve data from the cache if available."""
        hashed_key = hash_key(key)
        
        # Check for JSON data
        json_file = os.path.join(CACHE_DIR, f"{hashed_key}.json")
        if os.path.exists(json_file):
            with open(json_file, 'r') as file:
                return json.load(file)
        
        # Check for binary data
        bin_file = os.path.join(CACHE_DIR, f"{hashed_key}.bin")
        if os.path.exists(bin_file):
            with open(bin_file, 'rb') as file:
                return file.read()
        
        return None

    @staticmethod
    def set(key, data):
        """Save data to the cache."""
        hashed_key = hash_key(key)
        
        if isinstance(data, (bytes, bytearray)):
            # Binary data
            bin_file = os.path.join(CACHE_DIR, f"{hashed_key}.bin")
            with open(bin_file, 'wb') as file:
                file.write(data)
        else:
            # JSON data
            json_file = os.path.join(CACHE_DIR, f"{hashed_key}.json")
            with open(json_file, 'w') as file:
                json.dump(data, file, indent=4)

    @staticmethod
    def clear_cache():
        """Remove all cached files."""
        for filename in os.listdir(CACHE_DIR):
            file_path = os.path.join(CACHE_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

# Register the cache clearing function to be called on program exit
atexit.register(Cache.clear_cache)
