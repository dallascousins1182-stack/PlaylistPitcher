"""
PlaylistPitcher - Find and contact Spotify playlist owners for music promotion.
"""
print("🚀 APP.PY STARTING - This should appear in Railway logs!", flush=True)

import os
import streamlit as st
import spotipy
from dotenv import load_dotenv
from spotify_utils import initialize_spotify
from contact_extractor import extract_contact_info, format_contact_info

# Load environment variables
load_dotenv()

# Debug logging for Railway
print("Starting PlaylistPitcher...", flush=True)
print(f"Python version: {os.sys.version}", flush=True)
print(f"Current working directory: {os.getcwd()}", flush=True)
print(f"Environment variables loaded: SPOTIFY_CLIENT_ID={'✅' if os.getenv('SPOTIFY_CLIENT_ID') else '❌'}", flush=True)
print(f"Environment variables loaded: SPOTIFY_CLIENT_SECRET={'✅' if os.getenv('SPOTIFY_CLIENT_SECRET') else '❌'}", flush=True)

# Page configuration
st.set_page_config(
    page_title="PlaylistPitcher",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .stMetric {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("# 🎵 PlaylistPitcher")
st.markdown("**Find Spotify playlist owners and get their contact information**")
st.markdown("---")

# Sidebar for configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    # Get credentials from env or user input
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    # Debug: Show if credentials are loaded
    st.write(f"Client ID loaded: {'✅' if client_id else '❌'}")
    st.write(f"Client Secret loaded: {'✅' if client_secret else '❌'}")
    
    if not client_id or not client_secret:
        st.warning("⚠️ Spotify credentials not found in environment variables")
        client_id = st.text_input("Spotify Client ID", type="password", key="client_id")
        client_secret = st.text_input("Spotify Client Secret", type="password", key="client_secret")
        st.info("💡 **Tip:** Add credentials to `.env` file for auto-loading")
    else:
        st.success("✅ Spotify credentials loaded from environment")

# Main content
if client_id and client_secret:
    try:
        # Initialize Spotify client
        spotify = initialize_spotify(client_id, client_secret)
        
        # Search form
        col1, col2 = st.columns([3, 1])
        
        with col1:
            music_type = st.text_input(
                "🎸 What type of music are you looking for?",
                placeholder="e.g., lo-fi hip hop, ambient, indie rock, lo-fi anime",
                help="Enter a music genre or style to search for playlists"
            )
        
        with col2:
            num_results = st.slider(
                "Results",
                min_value=5,
                max_value=10,
                value=10,
                step=1,
                help="Number of playlists to search for (max 10)"
            )
        
        if music_type and music_type.strip():
            search_limit = max(1, min(50, int(num_results)))
            with st.expander("Debug: search parameters", expanded=False):
                st.write(f"Query: {music_type.strip()}")
                st.write(f"Limit: {search_limit} ({type(search_limit).__name__})")
            with st.spinner(f"🔍 Searching for '{music_type}' playlists..."):
                try:
                    playlists = spotify.search_playlists(music_type.strip(), limit=search_limit)
                    
                    if playlists:
                        st.success(f"Found {len(playlists)} playlists!")
                        st.markdown("---")
                        
                        # Display results
                        for idx, playlist in enumerate(playlists, 1):
                            with st.container():
                                col1, col2 = st.columns([4, 1])
                                
                                with col1:
                                    # Playlist header
                                    st.markdown(f"### {idx}. {playlist.get('name', 'Untitled')}")
                                    
                                    # Owner info
                                    owner = playlist.get('owner', {})
                                    owner_name = owner.get('display_name', 'Unknown')
                                    st.write(f"**Owner:** {owner_name}")
                                    
                                    # Playlist stats
                                    stats_col1, stats_col2, stats_col3 = st.columns(3)
                                    with stats_col1:
                                        st.metric("Followers", playlist.get('followers', {}).get('total', 0))
                                    with stats_col2:
                                        st.metric("Tracks", playlist.get('tracks', {}).get('total', 0))
                                    with stats_col3:
                                        is_public = "🔓 Public" if playlist.get('public') else "🔒 Private"
                                        st.write(is_public)
                                    
                                    # Description
                                    description = playlist.get('description', '')
                                    if description:
                                        st.write(f"**Description:** {description[:200]}...")
                                
                                with col2:
                                    if st.button("📋 View Contact Info", key=f"contact_{playlist['id']}"):
                                        st.session_state[f"show_{playlist['id']}"] = True
                                
                                # Show contact info if button was clicked
                                if st.session_state.get(f"show_{playlist['id']}", False):
                                    st.markdown("---")
                                    st.markdown("#### 📞 Contact Information")
                                    
                                    contact_info = extract_contact_info(playlist)
                                    contact_text = format_contact_info(contact_info)
                                    st.markdown(contact_text)
                                    
                                    # Copy buttons
                                    col1, col2, col3 = st.columns(3)
                                    
                                    if contact_info['profile_url']:
                                        with col1:
                                            st.markdown(
                                                f"[🔗 Open Spotify Profile]({contact_info['profile_url']})"
                                            )
                                    
                                    if contact_info['emails']:
                                        with col2:
                                            email = contact_info['emails'][0]
                                            st.write(f"📧 `{email}`")
                                    
                                    if contact_info['urls']:
                                        with col3:
                                            st.markdown(
                                                f"[🌐 Visit Website]({contact_info['urls'][0]})"
                                            )
                                
                                st.markdown("---")
                    
                    else:
                        st.warning(f"No playlists found for '{music_type}'. Try a different search term!")
                
                except spotipy.exceptions.SpotifyException as e:
                    st.error(f"❌ Spotify API Error: {e.http_status} - {getattr(e, 'msg', str(e))}")
                    st.error(f"Raw error: {repr(e)}")
                    st.info("💡 **Tips:** Check your credentials, try a different search term, or wait a moment and try again.")
                except Exception as e:
                    st.error(f"❌ Error searching playlists: {str(e)}")
                    st.error(f"Raw error: {repr(e)}")
                    st.info("💡 **Troubleshooting:** Make sure your Spotify API credentials are valid and try again.")
    
    except ValueError as e:
        st.error(f"❌ Configuration Error: {str(e)}")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

else:
    st.error("❌ Please provide Spotify credentials to continue")
    st.info("Add `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` to your `.env` file")
