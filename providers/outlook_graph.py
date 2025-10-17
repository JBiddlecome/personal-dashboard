# providers/outlook_graph.py
# Skeleton implementation for Outlook + Calendar using Microsoft Graph API
# OAuth flow to be implemented later
# This will provide access to Outlook emails and Microsoft Calendar events
Microsoft Graph for Outlook (Mail), Calendar, and optionally To Do.
Docs: https://learn.microsoft.com/graph/overview
Auth: OAuth 2.0 – app registration in Entra ID (Azure AD)
"""
from typing import List, Dict


# TODO: Initialize Graph client using stored OAuth tokens.




def get_outlook_unread() -> int:
# TODO: Call /me/mailFolders/Inbox/messages?$filter=isRead eq false&$count=true
return 0




def get_events_today() -> List[Dict]:
# TODO: Call /me/events with startDateTime/endDateTime for today
return []
