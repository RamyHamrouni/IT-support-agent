from app.schemas.chat import ChatResponse
from app.services.tools import manage_ticket
from app.schemas.chat import Message

async def handle_ticket(req, categories, args, attempts):
    ticket_response = manage_ticket(
        issue_code=args.get("issue_code"),
        issue_description=args.get("issue_description"),
        status=args.get("status"),
    )
    print(f"Ticket response: {ticket_response}")
    output = f"An open ticket has been created for your issue. Our support team will get back to you shortly."
    req.messages.append(Message(role="assistant", content=output))
    req.messages.append(Message(role="tool-call-output", content="An open ticket has been created for your issue. Our support team will get back to you shortly."))
    return ChatResponse(user_id=req.user_id, messages=req.messages)
