# ai-support-agent

AI customer support automation agent — a FastAPI service that classifies, drafts and routes support tickets using an LLM, with webhook integrations.

## What it does

- Receives a support ticket through a webhook intake endpoint.
- Classifies the ticket and drafts a reply with an LLM.
- Routes the ticket by category and priority, ready for a support workflow.

## Architecture

Ticket webhook -> FastAPI intake -> LLM classification and draft -> routing response. The service keeps the webhook, classification and routing steps separate so each part can be replaced or extended.

## Stack

- Python
- FastAPI
- OpenAI API
- Webhooks

## How to run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then send a ticket to `POST /webhooks/tickets`. Set `OPENAI_API_KEY` in the environment before using the LLM classification step.
