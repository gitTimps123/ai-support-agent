import os
from enum import Enum

from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel

app = FastAPI(title="ai-support-agent")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Ticket(BaseModel):
    id: str
    subject: str
    message: str
    customer_email: str | None = None


class TicketResult(BaseModel):
    ticket_id: str
    category: str
    priority: Priority
    draft_reply: str
    route: str


def classify_ticket(ticket: Ticket) -> tuple[str, Priority, str]:
    """Classify a ticket and draft a reply with an LLM."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Classify support tickets and draft a short, helpful reply."},
            {"role": "user", "content": f"Subject: {ticket.subject}\nMessage: {ticket.message}"},
        ],
    )
    text = response.choices[0].message.content or ""
    return "general", Priority.medium, text


def route_for(category: str, priority: Priority) -> str:
    if priority == Priority.high:
        return "urgent-support"
    return f"support-{category}"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/webhooks/tickets", response_model=TicketResult)
def ticket_webhook(ticket: Ticket):
    category, priority, draft_reply = classify_ticket(ticket)
    return TicketResult(
        ticket_id=ticket.id,
        category=category,
        priority=priority,
        draft_reply=draft_reply,
        route=route_for(category, priority),
    )
