#!/usr/bin/env python3
"""
Test MP3 conversion specifically
"""

import requests
import time

def test_mp3_download():
    """Test MP3 download and conversion"""
    
    base_url = "http://localhost:8000"
    
    # Test URL (short video)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print("🧪 Testing MP3 Download...")
    print("=" * 50)
    
    # Test MP3 download
    print("🎵 Testing MP3 download...")
    try:
        data = {
            "url": test_url,
            "format_type": "mp3"
        }
        
        print(f"   Downloading: {test_url}")
        response = requests.post(f"{base_url}/download", data=data, timeout=60)
        
        if response.status_code == 200:
            print("✅ MP3 download successful")
            print(f"   File size: {len(response.content)} bytes")
            
            # Check if it's actually MP3
            content_type = response.headers.get('content-type', '')
            if 'audio' in content_type or 'octet-stream' in content_type:
                print("✅ File appears to be audio format")
            else:
                print(f"⚠️  Content-Type: {content_type}")
            
            return True
        else:
            print(f"❌ MP3 download failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ MP3 download failed: {e}")
        return False

if __name__ == "__main__":
    if test_mp3_download():
        print("\n🎉 MP3 download is working!")
        print("🌐 Open http://localhost:8000 in your browser to use it.")
    else:
        print("\n❌ MP3 download still has issues.")
