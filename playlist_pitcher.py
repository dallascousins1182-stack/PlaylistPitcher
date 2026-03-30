import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from collections import defaultdict


class PlaylistPitcher:
    def __init__(self, client_id, client_secret):
        """Initialize Spotify API connection"""
        self.client_id = client_id
        self.client_secret = client_secret
        self.sp = None
        self.connect()
    
    def connect(self):
        """Connect to Spotify API"""
        try:
            auth_manager = SpotifyClientCredentials(
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            print("✓ Successfully connected to Spotify API")
        except Exception as e:
            print(f"✗ Error connecting to Spotify: {e}")
            raise
    
    def search_playlists(self, music_type, limit=50):
        """
        Search for playlists matching the music type
        
        Args:
            music_type (str): Genre or type of music to search for
            limit (int): Number of playlists to fetch
            
        Returns:
            list: List of playlist objects
        """
        try:
            print(f"\n🔍 Searching for '{music_type}' playlists...")
            results = self.sp.search(
                q=f"genre:{music_type}",
                type='playlist',
                limit=limit
            )
            playlists = results.get('playlists', {}).get('items', [])
            print(f"✓ Found {len(playlists)} playlists")
            return playlists
        except Exception as e:
            print(f"✗ Error searching playlists: {e}")
            return []
    
    def get_playlist_owners(self, playlists):
        """
        Extract owner information from playlists
        
        Args:
            playlists (list): List of playlist objects
            
        Returns:
            dict: Owner information organized by owner name
        """
        owners_data = defaultdict(list)
        
        for playlist in playlists:
            try:
                owner = playlist.get('owner', {})
                owner_name = owner.get('display_name', 'Unknown')
                owner_id = owner.get('id', 'N/A')
                owner_url = owner.get('external_urls', {}).get('spotify', 'N/A')
                
                playlist_data = {
                    'playlist_name': playlist.get('name', 'Unknown'),
                    'playlist_url': playlist.get('external_urls', {}).get('spotify', 'N/A'),
                    'owner_name': owner_name,
                    'owner_id': owner_id,
                    'owner_url': owner_url,
                    'followers': playlist.get('followers', {}).get('total', 0),
                    'tracks': playlist.get('tracks', {}).get('total', 0)
                }
                
                owners_data[owner_name].append(playlist_data)
            except Exception as e:
                print(f"⚠ Error processing playlist: {e}")
                continue
        
        return dict(owners_data)
    
    def display_results(self, owners_data):
        """
        Display owner and playlist information in a formatted way
        
        Args:
            owners_data (dict): Owner information
        """
        if not owners_data:
            print("\n✗ No playlists found")
            return
        
        print(f"\n{'='*80}")
        print(f"PLAYLIST OWNERS FOUND: {len(owners_data)}")
        print(f"{'='*80}\n")
        
        for idx, (owner_name, playlists) in enumerate(owners_data.items(), 1):
            print(f"\n[{idx}] Owner: {owner_name}")
            print(f"    Playlists: {len(playlists)}")
            print(f"    {'-'*76}")
            
            for playlist in playlists:
                print(f"    • {playlist['playlist_name']}")
                print(f"      URL: {playlist['playlist_url']}")
                print(f"      Followers: {playlist['followers']} | Tracks: {playlist['tracks']}")
                print()
    
    def export_to_json(self, owners_data, filename='playlist_owners.json'):
        """
        Export owner data to JSON file
        
        Args:
            owners_data (dict): Owner information
            filename (str): Output filename
        """
        try:
            with open(filename, 'w') as f:
                json.dump(owners_data, f, indent=2)
            print(f"\n✓ Results exported to {filename}")
        except Exception as e:
            print(f"✗ Error exporting data: {e}")
    
    def run(self, music_type):
        """
        Main execution method
        
        Args:
            music_type (str): Genre or type of music to search for
        """
        try:
            # Search for playlists
            playlists = self.search_playlists(music_type, limit=50)
            
            if not playlists:
                print("No playlists found. Try a different music type.")
                return
            
            # Get owner information
            owners_data = self.get_playlist_owners(playlists)
            
            # Display results
            self.display_results(owners_data)
            
            # Export results
            self.export_to_json(owners_data)
            
        except Exception as e:
            print(f"✗ Error during execution: {e}")


def main():
    # Spotify API credentials
    CLIENT_ID = "caa25c3e120341c78cccd697763c3081"
    CLIENT_SECRET = "3052307e5f324ce29adf2c36ebf66342"
    
    # Initialize the app
    pitcher = PlaylistPitcher(CLIENT_ID, CLIENT_SECRET)
    
    # Get music type from user
    print("\n" + "="*80)
    print("🎵 PLAYLIST PITCHER - Find Spotify Playlist Owners 🎵")
    print("="*80)
    
    music_type = input("\nEnter the type of music you're interested in (e.g., 'rock', 'hip-hop', 'lo-fi'): ").strip()
    
    if not music_type:
        print("✗ No music type entered. Exiting.")
        return
    
    # Run the search
    pitcher.run(music_type)


if __name__ == "__main__":
    main()
