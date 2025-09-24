#!/usr/bin/env python3
"""
Simple script to start the Universal Downloader
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import yt_dlp
        import uvicorn
        print("✅ All Python dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_ffmpeg():
    """Check if FFmpeg is installed (optional for MP3 conversion)"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ FFmpeg is installed (optional)")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("ℹ️  FFmpeg not found - using pydub for MP3 conversion instead")
    return True  # Always allow to continue

def main():
    print("🚀 Starting Universal Downloader...")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    if not check_ffmpeg():
        sys.exit(1)
    
    # Create downloads directory
    os.makedirs("downloads", exist_ok=True)
    print("✅ Downloads directory ready")
    
    print("\n🌐 Starting server...")
    print("   URL: http://localhost:8000")
    print("   Press Ctrl+C to stop")
    print("=" * 40)
    
    try:
        # Start the server
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")

if __name__ == "__main__":
    main()
