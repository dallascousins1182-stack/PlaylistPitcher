"""
Extract contact information from Spotify playlist descriptions and owner profiles.
"""
import re
from typing import Dict, List


def extract_emails(text: str) -> List[str]:
    """Extract email addresses from text."""
    if not text:
        return []
    
    # Email regex pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return list(set(emails))  # Remove duplicates


def extract_urls(text: str) -> List[str]:
    """Extract URLs from text."""
    if not text:
        return []
    
    # URL regex pattern
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, text)
    return list(set(urls))  # Remove duplicates


def extract_contact_info(playlist: Dict) -> Dict:
    """
    Extract all contact information from a playlist and owner.
    
    Args:
        playlist: Spotify playlist object from API
        
    Returns:
        Dictionary with contact information
    """
    contact_info = {
        'profile_url': None,
        'spotify_dm_link': None,
        'emails': [],
        'urls': [],
        'description_text': None
    }
    
    # Get owner profile URL
    if 'owner' in playlist and playlist['owner']:
        owner = playlist['owner']
        external_urls = owner.get('external_urls', {})
        if 'spotify' in external_urls:
            contact_info['profile_url'] = external_urls['spotify']
            # Generate DM link (Spotify web format)
            owner_id = owner.get('id')
            if owner_id:
                contact_info['spotify_dm_link'] = f"https://open.spotify.com/user/{owner_id}"
    
    # Extract from description
    description = playlist.get('description', '')
    if description:
        contact_info['description_text'] = description
        contact_info['emails'] = extract_emails(description)
        contact_info['urls'] = extract_urls(description)
    
    return contact_info


def format_contact_info(contact_info: Dict) -> str:
    """Format contact information for display."""
    output = []
    
    if contact_info['profile_url']:
        output.append(f"🎵 **Spotify Profile:** {contact_info['profile_url']}")
    
    if contact_info['spotify_dm_link']:
        output.append(f"💬 **Spotify DM Link:** {contact_info['spotify_dm_link']}")
    
    if contact_info['emails']:
        emails_str = ', '.join(contact_info['emails'])
        output.append(f"📧 **Email(s):** {emails_str}")
    
    if contact_info['urls']:
        for url in contact_info['urls']:
            output.append(f"🔗 **Link:** {url}")
    
    if contact_info['description_text']:
        output.append(f"\n**Description:** {contact_info['description_text']}")
    
    return '\n\n'.join(output) if output else "No contact information found"
