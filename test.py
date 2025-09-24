#!/usr/bin/env python3
"""
Simple test to verify downloader works
"""

import requests
import time

def test_download():
    """Test the downloader with a simple URL"""
    
    base_url = "http://localhost:8000"
    
    # Test URL (short video)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print("🧪 Testing Universal Downloader...")
    print("=" * 50)
    
    # Test 1: Health check
    print("1️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Download test (MP4)
    print("\n2️⃣ Testing MP4 download...")
    try:
        data = {
            "url": test_url,
            "format_type": "mp4"
        }
        
        print(f"   Downloading: {test_url}")
        response = requests.post(f"{base_url}/download", data=data, timeout=60)
        
        if response.status_code == 200:
            print("✅ MP4 download successful")
            print(f"   File size: {len(response.content)} bytes")
            return True
        else:
            print(f"❌ MP4 download failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ MP4 download failed: {e}")
        return False

if __name__ == "__main__":
    if test_download():
        print("\n🎉 Downloader is working perfectly!")
        print("🌐 Open http://localhost:8000 in your browser to use it.")
    else:
        print("\n❌ There are still issues to fix.")
