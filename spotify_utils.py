"""
Spotify API utilities for searching playlists and extracting owner information.
"""
import os
import sys
from typing import List, Dict
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyClient:
    """Wrapper for Spotify API interactions."""
    
    def __init__(self, client_id: str = None, client_secret: str = None):
        """
        Initialize Spotify client.
        
        Args:
            client_id: Spotify API client ID (uses env var if not provided)
            client_secret: Spotify API client secret (uses env var if not provided)
        """
        self.client_id = client_id or os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('SPOTIFY_CLIENT_SECRET')
        
        if not self.client_id or not self.client_secret:
            raise ValueError(
                "Spotify credentials not found. Set SPOTIFY_CLIENT_ID and "
                "SPOTIFY_CLIENT_SECRET environment variables."
            )
        
        try:
            auth_manager = SpotifyClientCredentials(
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            print(f"[DEBUG] Spotipy initialized successfully", file=sys.stderr)
        except Exception as e:
            raise ValueError(f"Failed to initialize Spotify client: {str(e)}")
    
    def search_playlists(self, query: str, limit: int = 50) -> List[Dict]:
        """
        Search for playlists by keyword.
        
        Args:
            query: Search query (e.g., "lo-fi hip hop", "ambient")
            limit: Maximum number of results (1-50)
            
        Returns:
            List of playlist objects
        """
        try:
            # Validate limit
            limit = int(limit)
            if limit < 1:
                limit = 1
            elif limit > 50:
                limit = 50
            
            print(f"[DEBUG] Searching: query='{query}', limit={limit} (type: {type(limit).__name__})", file=sys.stderr)
            
            # Use direct API call instead of spotipy search
            import requests
            
            # Get fresh access token
            try:
                # Try to refresh token if needed
                token_info = self.sp.auth_manager.get_access_token(as_dict=True)
                access_token = token_info.get('access_token') if token_info else None
                print(f"[DEBUG] Token info: {bool(token_info)}, access_token: {bool(access_token)}", file=sys.stderr)
                if not access_token:
                    raise ValueError("No access token available")
            except Exception as e:
                print(f"[DEBUG] Token error: {e}", file=sys.stderr)
                raise ValueError(f"Failed to get access token: {e}")
            
            url = "https://api.spotify.com/v1/search"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            params = {
                "q": query,
                "type": "playlist", 
                "limit": str(limit),
                "offset": "0"
            }
            
            print(f"[DEBUG] Final URL: {requests.Request('GET', url, headers=headers, params=params).prepare().url}", file=sys.stderr)
            print(f"[DEBUG] Headers: {headers}", file=sys.stderr)
            
            response = requests.get(url, headers=headers, params=params)
            print(f"[DEBUG] Response status: {response.status_code}", file=sys.stderr)
            print(f"[DEBUG] Response headers: {dict(response.headers)}", file=sys.stderr)
            
            if response.status_code != 200:
                print(f"[DEBUG] Error response body: {response.text}", file=sys.stderr)
                try:
                    error_data = response.json()
                    print(f"[DEBUG] Error JSON: {error_data}", file=sys.stderr)
                except:
                    print(f"[DEBUG] Error text: {response.text}", file=sys.stderr)
                response.raise_for_status()
            
            data = response.json()
            playlists = data.get('playlists', {}).get('items', [])
            print(f"[DEBUG] Found {len(playlists)} playlists", file=sys.stderr)
            return playlists
            
        except requests.exceptions.RequestException as e:
            print(f"[DEBUG] RequestException: {e}", file=sys.stderr)
            raise ValueError(f"Spotify API Error: {str(e)}")
        except Exception as e:
            print(f"[DEBUG] Exception: {type(e).__name__}: {str(e)}", file=sys.stderr)
            raise ValueError(f"Failed to search playlists: {str(e)}")
    
    def get_playlist_details(self, playlist_id: str) -> Dict:
        """
        Get detailed information about a playlist.
        
        Args:
            playlist_id: Spotify playlist ID
            
        Returns:
            Detailed playlist object
        """
        return self.sp.playlist(playlist_id)
    
    def get_playlist_tracks(self, playlist_id: str, limit: int = 50) -> List[Dict]:
        """
        Get tracks from a playlist.
        
        Args:
            playlist_id: Spotify playlist ID
            limit: Maximum number of tracks to fetch
            
        Returns:
            List of track objects
        """
        results = self.sp.playlist_tracks(playlist_id, limit=limit)
        return results['items']
    
    def get_audio_features(self, track_ids: List[str]) -> List[Dict]:
        """
        Get audio features for tracks (for similarity analysis).
        
        Args:
            track_ids: List of Spotify track IDs
            
        Returns:
            List of audio feature objects
        """
        if not track_ids:
            return []
        
        # Spotify API limits to 100 IDs per request
        features = []
        for i in range(0, len(track_ids), 100):
            batch = track_ids[i:i+100]
            batch_features = self.sp.audio_features(*batch)
            features.extend([f for f in batch_features if f])
        
        return features


def initialize_spotify(client_id: str, client_secret: str) -> SpotifyClient:
    """Initialize and return a Spotify client."""
    return SpotifyClient(client_id=client_id, client_secret=client_secret)
