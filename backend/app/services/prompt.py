# app/services/prompt.py
from app.utils.yaml_loader import load_yaml

prompts = load_yaml("prompt.yaml")

def build_prompt(messages: list[dict[str, str]], categories: list[str]) -> str:
    system = prompts["system_prompt"]
    workflow = prompts["workflow_instructions"].format(categories=", ".join(categories))

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



