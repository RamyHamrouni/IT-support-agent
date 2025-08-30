from app.services.tools import query_knowledge_base
from app.schemas.chat import ChatResponse, Message
from app.services.response_formatter import format_kb_results

async def handle_knowledge_base(req, categories, args, attempts):
    if attempts >= 1:
        output = "I couldn’t find a relevant case. Would you like me to escalate this issue?"
        req.messages.append(Message(role="assistant", content=output))
        return ChatResponse(messages=req.messages)

    from app.services.chat_service import process_chat

    query = args.get("query")
    type_issue = args.get("type_issue")

    results = query_knowledge_base(query=query, max_results=3, type_issue=type_issue)
    print(results)

    if len(results) == 0:
        output = "I couldn’t find a relevant case. Would you like me to escalate this issue?"
        req.messages.append(Message(role="assistant", content=output))
        req.messages.append(Message(role="tool-call-output", content="No results were retrieved from the knowledge base."))
        return ChatResponse(messages=req.messages)
    if max(r.score for r in results) <= 0.2:
        output = "I couldn’t find a relevant case. Would you like me to escalate this issue?"
        req.messages.append(Message(role="assistant", content=output))
        req.messages.append(Message(role="tool-call-output", content="The retrieved knowledge base results are not relevant enough."))
        return ChatResponse(messages=req.messages)
    mapped = [
        {"question": r.payload.get("question"), "answer": r.payload.get("answer"), "confidence":r.score}
        for r in results
    ]
    formatted = format_kb_results(mapped)
    instruction = "You have already retrieved knowledge base results. Do not call the knowledge base tool again.Answer the user's question based on the knowledge base results."

    req.messages.append(Message(role="system", content=instruction))
    req.messages.append(Message(role="tool-call-output", content=formatted))


    return await process_chat(req, categories, attempts + 1)
