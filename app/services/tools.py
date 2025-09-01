from app.utils.yaml_loader import load_yaml
from app.db.qdrant_client import QdrantWrapper

tools_config = load_yaml("tools.yaml")

def get_tools(categories: list[str]):
    tools = tools_config.get("tools", [])
    print(f"Available tools: {[tool['function']['name'] for tool in tools if 'function' in tool]}")

    for tool in tools:
        if "function" not in tool:
            continue  # skip if not a function tool

        func = tool["function"]
        if "parameters" not in func:
            continue

        props = func["parameters"].get("properties", {})

        # inject categories into type_issue
        if "type_issue" in props:
            props["type_issue"]["enum"] = categories

    return tools
def query_knowledge_base(query:str,max_results:int,type_issue:str):
    embedding = load_yaml("embedding.yaml")
    kb_vector_search = QdrantWrapper(collection_name="kb_collection",
                               embedding_model=embedding.get('embedding_model').get('default_model'), 
                               embedding_dim=embedding.get("embedding_model", {}).get("params", {}).get("embedding_dim"))
    results = kb_vector_search.query(query=query,max_results=max_results,metadata_key="category",metadata_value=type_issue)
    return results
def query_guide_issue(query:str,max_results:int,type_issue:str):
    embedding = load_yaml("embedding.yaml")
    kb_vector_search = QdrantWrapper(collection_name="guide_collection",
                               embedding_model=embedding.get('embedding_model').get('default_model'), 
                               embedding_dim=embedding.get("embedding_model", {}).get("params", {}).get("embedding_dim"))
    results = kb_vector_search.query(query=query,max_results=max_results,metadata_key="category",metadata_value=type_issue)
    return results
def manage_ticket(issue_code:str,issue_description:str,status:str):
    import requests
    from dotenv import load_dotenv
    import os
    load_dotenv()
    DB_URL = os.getenv("DB_URL")
    payload = {
        "description": issue_description,
        "status": status,
        "user":"user-123"
    }
    print(f"Managing ticket with payload: {payload}")
    try:
        resp = requests.post(f"{DB_URL}/tickets", json=payload)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"Error managing ticket: {e}")
        return {"error": str(e)}