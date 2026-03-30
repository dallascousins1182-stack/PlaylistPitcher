# 🎵 PlaylistPitcher

Find Spotify playlist owners and get their contact information for music promotion.

## Features

✅ **Playlist Discovery** - Search for playlists by music genre/type  
✅ **Owner Contact Info** - Extract Spotify profile URLs and DM links  
✅ **Email Extraction** - Automatically find emails in playlist descriptions  
✅ **Link Discovery** - Extract URLs from playlist descriptions  
✅ **Secure Credentials** - Environment variable support for API keys  

## Quick Start

### 1. Clone or Setup Project

```bash
cd PlaylistPitcher
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Spotify credentials:

```
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

**Get Spotify API credentials:**
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create an app
3. Accept terms and copy your Client ID and Client Secret
4. Add them to `.env`

### 4. Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## How to Use

1. **Enter Music Type** - Type in a music genre or style (e.g., "lo-fi hip hop", "ambient", "indie rock")
2. **Adjust Results** - Set how many playlists to search (5-50)
3. **Click "View Contact Info"** - See owner's Spotify profile, DM link, and any emails/URLs in description
4. **Reach Out** - Use the contact information to pitch your music

## Project Structure

```
PlaylistPitcher/
├── app.py                 # Main Streamlit application
├── spotify_utils.py       # Spotify API client & utilities
├── contact_extractor.py   # Email/URL extraction logic
├── requirements.txt       # Python dependencies
├── .env                   # Your credentials (not in git)
├── .env.example          # Template for credentials
├── .gitignore            # Ignore sensitive files
└── README.md             # This file
```

## API Information

- **Spotify Web API** - Used for playlist search and owner data
- **Rate Limits** - 429 errors handled gracefully
- **Data** - Only uses publicly available playlist information

## Troubleshooting

**"Spotify credentials not found"**
- Make sure `.env` file is in the same directory as `app.py`
- Verify environment variables are set correctly

**"No playlists found"**
- Try different search terms
- Spotify search is keyword-based, so be specific

**"No contact information found"**
- Owner may not have public email or links in description
- Profile URL and Spotify DM link are always available

## Privacy & Security

- **Never commit `.env` file** - It's in `.gitignore`
- **Credentials are not logged** - Only used for API authentication
- **No data collection** - This app doesn't store user searches

## Next Steps

- 🚀 Deploy to Streamlit Cloud or Heroku
- 📊 Add playlist analytics (follower trends, track analysis)
- 🤖 Implement AI-powered playlist similarity (audio features)
- 💾 Add CSV export for playlist batches
- 🔐 Add user authentication

## License

MIT - Feel free to use and modify

## Support

For issues or questions, check the Spotify API documentation: https://developer.spotify.com/documentation/web-api

Enter the type of music you're interested in (e.g., 'rock', 'hip-hop', 'lo-fi'): lo-fi
✓ Successfully connected to Spotify API

🔍 Searching for 'lo-fi' playlists...
✓ Found 50 playlists

================================================================================
PLAYLIST OWNERS FOUND: 45
================================================================================
```

## Notes

- The app uses Spotify's Client Credentials flow for API access
- Results include playlist URLs, owner profiles, and follower counts
- The JSON export allows you to process results programmatically
