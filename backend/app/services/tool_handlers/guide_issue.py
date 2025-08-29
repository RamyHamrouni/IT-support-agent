from app.schemas.chat import ChatResponse, Message
from app.services.tools import query_guide_issue
from app.services.response_formatter import format_issue_guide_results

async def handle_issue_guide(req, categories, args, attempts):
    from app.services.chat_service import process_chat
    query = args.get("query")
    type_issue = args.get("type_issue")

    results = query_guide_issue(query=query, max_results=3, type_issue=type_issue)
    if len(results) == 0:
        req.messages.append(Message(role="assistant", content="No results were retrieved from the issue guide."))
        if attempts >= 1:
            return ChatResponse(reply="I couldn’t find a relevant guide. Would you like me to escalate this issue?")
        return await process_chat(req, categories, attempts + 1)

    mapped = [
        {
            "issue": r.payload.get("issue"),
            "troublshouting_steps": r.payload.get("troubleshooting_steps"),
            "quick_fixes": r.payload.get("quick_fixes"),
            "escalation_criteria": r.payload.get("escalation_criteria"),
            "score": r.score,
        }
        for r in results
    ]
    print(mapped)
    formatted = format_issue_guide_results(mapped)
    req.messages.append(Message(role="assistant", content=formatted))
    return await process_chat(req, categories, attempts)
