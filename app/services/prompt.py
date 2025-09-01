# app/services/prompt.py
from app.utils.yaml_loader import load_yaml
from app.db.database_client import fetch_tickets


prompts = load_yaml("prompt.yaml")

def build_prompt(messages: list[dict[str, str]], user_id: str, categories: list[str]) -> str:
    tickets = fetch_tickets(user_id)
    print("tickets", tickets)
    
    # Handle different return types from get_tickets_by_user
    if isinstance(tickets, dict) and "error" in tickets:
        # Error response - no tickets found
        formatted_tickets = "No tickets found"
    elif isinstance(tickets, list) and len(tickets) > 0:
        # Success response with tickets
        formatted_tickets = "\n".join([f"Ticket ID: {ticket['id']}\nTicket Description: {ticket['description']}\nTicket Status: {ticket['status']}" for ticket in tickets])
    else:
        # Empty list or other case
        formatted_tickets = "No tickets found"

    system = prompts["system_prompt"]
    workflow = prompts["workflow_instructions"].format(categories=", ".join(categories), tickets=formatted_tickets)

    convo = []
    for m in messages:
        role = m.get("role", "user").upper()
        content = m.get("content", "")
        if role == "SYSTEM":
            system = content
        else:
            convo.append(f"{role}: {content}")
    
    prompt_text = (
        f"<SYSTEM>\n{system}\n{workflow}\n</SYSTEM>\n\n"
        f"{convo}\nASSISTANT:"
    )
    print("prompt_text", prompt_text)
    return prompt_text



