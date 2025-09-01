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


def create_ticket(issue_code: str, issue_description: str, status: str, user: str = "user-123") -> dict:
    """Create a new ticket in the external DB."""
    try:
        payload = {
            "description": issue_description,
            "status": status,
        }
        print(f"Creating ticket with payload: {payload}")
        try:
            resp = requests.post(f"{DB_URL}/tickets/{user}", json=payload)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"Error creating ticket: {e}")
            payload = {
                "description": issue_description,
                "status": status,
            }
            print(f"Creating ticket with payload: {payload}")
            resp = requests.post(f"{DB_URL}/tickets/{user}", json=payload)
            resp.raise_for_status()
            return {"error": str(e)}
        
        ticket_data = resp.json()
        print(f"Ticket created successfully: {ticket_data}")
        return ticket_data
    except requests.RequestException as e:
        print(f"Error creating ticket: {e}")
        return {"error": str(e)}
