import json
from app.services.tool_handlers import knowledge_base, guide_issue, ticket


async def handle_tool_call(req, categories, tool_calls, attempts):
    call = tool_calls[0]
    fn = call.function.name
    args = json.loads(call.function.arguments)

    handlers = {
        "query_knowledge_base": knowledge_base.handle_knowledge_base,
        "query_issue_guide": guide_issue.handle_issue_guide,
        "manage_ticket": ticket.handle_ticket,
    }

    if fn not in handlers:
        raise ValueError(f"Unsupported tool: {fn}")

    return await handlers[fn](req, categories, args, attempts)
