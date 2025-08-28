from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import json

app = FastAPI()
allowed_origins = ["*"]
app.add_middleware(
CORSMiddleware,
allow_origins=[o.strip() for o in allowed_origins],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

class Ticket(BaseModel):
    user: str
    issue_code: str
    description: str
    status: str = "open"   # default status


with open("db.json", "r") as f:
    db = json.load(f)

@app.get("/")
def root():
    return {"message": "Knowledge Base API is running 🚀"}

@app.get("/kb")
def get_kb():
    return db["kb"]
@app.get("/user")
def get_kb():
    return db["user"]
@app.get("/user/{user_id}")
def get_user_by_id(user_id: str):
    for user in db["user"]:
        if user["id"] == user_id:
            return user
    return {"error": "Not found"}

@app.get("/guide")
def get_guides():
    return db["guide"]

@app.get("/tickets")
def get_tickets():
    return db["tickets"]
@app.post("/tickets")
def create_ticket(ticket: Ticket):
    new_ticket = {
        "id": f"TICKET-{len(db['tickets']) + 1:03d}",
        "user": ticket.user,
        "issue_code": ticket.issue_code,
        "description": ticket.description,
        "status": ticket.status
    }
    db["tickets"].append(new_ticket)

    # save back to file (optional, otherwise lost when app restarts)
    with open("db.json", "w") as f:
        json.dump(db, f, indent=2)

    return {"message": "Ticket created successfully ✅", "ticket": new_ticket}



@app.get("/kb/{issue_code}")
def get_kb_by_code(issue_code: str):
    for item in db["kb"]:
        if item["issue_code"] == issue_code:
            return item
    return {"error": "Not found"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)

