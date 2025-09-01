import requests
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL")


def fetch_kb_data() -> list[dict]:
    """Fetch Knowledge Base entries from external DB."""
    try:
        resp = requests.get(f"{DB_URL}/kb")
        resp.raise_for_status()
        kb_data = resp.json()
        print(f"Fetched {len(kb_data)} Knowledge Database entries")
        return kb_data
    except requests.RequestException as e:
        print(f"Error fetching KB data: {e}")
        return []


def fetch_guide_data() -> list[dict]:
    """Fetch Guide entries from external DB."""
    try:
        resp = requests.get(f"{DB_URL}/guide")
        resp.raise_for_status()
        guide_data = resp.json()
        print(f"Fetched {len(guide_data)} Guide entries")
        return guide_data
    except requests.RequestException as e:
        print(f"Error fetching Guide data: {e}")
        return []
def fetch_tickets(user_id: str) -> list[dict]:
    """Fetch tickets from external DB."""
    try:
        resp = requests.get(f"{DB_URL}/tickets/{user_id}")
        resp.raise_for_status()
        tickets = resp.json()
        print(f"Fetched {len(tickets)} tickets")
        return tickets
    except requests.RequestException as e:
        print(f"Error fetching tickets: {e}")
        return []
