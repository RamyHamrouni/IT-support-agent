from app.services.tools import query_knowledge_base
from app.schemas.chat import ChatResponse, Message
from app.services.tools import query_knowledge_base
from app.services.response_formatter import format_kb_results

async def handle_knowledge_base(req, categories, args, attempts):
    from app.services.chat_service import process_chat
    query = args.get("query")
    type_issue = args.get("type_issue")

    results = query_knowledge_base(query=query, max_results=3, type_issue=type_issue)
    if len(results) == 0:
        
        req.messages.append(Message(role="assistant", content="No results were retrieved from the knowledge base."))
        if attempts >= 1:
            return ChatResponse(reply="I couldn’t find relevant documentation. Would you like me to escalate this issue?")
        
        return await process_chat(req, categories, attempts + 1)

    mapped = [
        {"question": r.payload.get("question"), "answer": r.payload.get("answer"), "score": r.score}
        for r in results
    ]
    formatted = format_kb_results(mapped)
    req.messages.append(Message(role="assistant", content=formatted))
    return await process_chat(req, categories, attempts)