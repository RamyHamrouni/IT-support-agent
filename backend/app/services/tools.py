from app.utils.yaml_loader import load_yaml

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