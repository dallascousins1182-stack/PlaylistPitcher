#!/usr/bin/env python3
"""
Simple test script to verify Railway deployment
"""
import os
import sys

print("=== PlaylistPitcher Railway Test ===", flush=True)
print(f"Python version: {sys.version}", flush=True)
print(f"Working directory: {os.getcwd()}", flush=True)

try:
    import streamlit
    print("✅ Streamlit imported successfully", flush=True)
except ImportError as e:
    print(f"❌ Streamlit import failed: {e}", flush=True)

try:
    import spotipy
    print("✅ Spotipy imported successfully", flush=True)
except ImportError as e:
    print(f"❌ Spotipy import failed: {e}", flush=True)

try:
    from dotenv import load_dotenv
    print("✅ python-dotenv imported successfully", flush=True)
except ImportError as e:
    print(f"❌ python-dotenv import failed: {e}", flush=True)

# Check environment variables
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
print(f"SPOTIFY_CLIENT_ID: {'✅ Set' if client_id else '❌ Not set'}", flush=True)
print(f"SPOTIFY_CLIENT_SECRET: {'✅ Set' if client_secret else '❌ Not set'}", flush=True)

print("=== Test Complete ===", flush=True)