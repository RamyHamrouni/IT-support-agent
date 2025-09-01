from app.schemas.chat import ChatResponse, Message
from app.services.tools import query_guide_issue
from app.services.response_formatter import format_issue_guide_results

async def handle_issue_guide(req, categories, args, attempts):
    if attempts >= 1:
        output = "I couldn’t find a relevant guide. Would you like me to escalate this issue?"
        req.messages.append(Message(role="assistant", content=output))
        return ChatResponse(messages=req.messages)

    from app.services.chat_service import process_chat

    query = args.get("query")
    type_issue = args.get("type_issue")

    results = query_guide_issue(query=query, max_results=3, type_issue=type_issue)

    if len(results) == 0:
        output = "I couldn’t find a relevant guide. Would you like me to escalate this issue?"
        req.messages.append(Message(role="assistant", content=output))
        req.messages.append(Message(role="tool-call-output", content="No results were retrieved from the issue guide."))
        return ChatResponse(user_id=req.user_id, messages=req.messages)
    print(results)
    scores = [r.score for r in results]
    max_score = max(scores)
    if max_score <= 0.2:
        output = "I couldn’t find a relevant guide. Would you like me to escalate this issue?"
        req.messages.append(Message(role="assistant", content=output))
        req.messages.append(Message(role="tool-call-output", content="The retrieved guide results are not relevant enough."))
        return ChatResponse(user_id=req.user_id, messages=req.messages)
    filtered_results = [r for r in results if r.score > 0.2]
    mapped = [
        {
            "issue": r.payload.get("issue"),
            "troubleshooting_steps": r.payload.get("troubleshooting_steps"),
            "quick_fixes": r.payload.get("quick_fixes"),
            "escalation_criteria": r.payload.get("escalation_criteria"),
            "confidence": r.score,
        }
        for r in filtered_results
    ]
    formatted = format_issue_guide_results(mapped)
    instruction = "You have already retrieved issue guide results. Do not call the issue guide tool again.Answer the user's question based on the issue guide results."
    req.messages.append(Message(role="system", content=instruction))
    req.messages.append(Message(role="tool-call-output", content=formatted))

 
    return await process_chat(req, categories, attempts + 1)
