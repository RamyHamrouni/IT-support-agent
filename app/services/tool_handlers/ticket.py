from app.schemas.chat import ChatResponse
from app.services.tools import manage_ticket
from app.schemas.chat import Message

async def handle_ticket(req, args):
    ticket_response = manage_ticket(
        issue_code=args.get("issue_code"),
        issue_description=args.get("issue_description"),
        status=args.get("status"),
        user=req.user_id,
    )
    print(f"Ticket response: {ticket_response}")
    if ticket_response.get("error"):
        output = f"An error occurred while creating the ticket. Would you like to try again?"
        req.messages.append(Message(role="assistant", content=output))
        req.messages.append(Message(role="tool-call-output", content=f"An error occurred while creating the ticket. Please try again."))
        return ChatResponse(user_id=req.user_id, messages=req.messages)
    else:
        output = f"An open ticket has been created for your issue. Our support team will get back to you shortly."
    req.messages.append(Message(role="assistant", content=output))
    req.messages.append(Message(role="tool-call-output", content="An open ticket has been created for your issue. Our support team will get back to you shortly."))
    return ChatResponse(user_id=req.user_id, messages=req.messages)
