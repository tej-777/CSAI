from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field, ValidationError
from agents.router_agent import route_query
from agents.summarizer_agent import summarize_output
from agents.critic_agent import provide_feedback
from agents.feedback_manager import store_feedback
from database.db_manager import DatabaseManager
from utils.logger import logger
from config import settings


class QueryPayload(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
from config import settings

app = FastAPI()
db = DatabaseManager()


@app.post("/query")
async def handle_query(request: Request):
    try:
        payload = await request.json()
        data = QueryPayload(**payload)
    except ValidationError as ve:
        logger.warning("Invalid payload for /query: %s", ve)
        raise HTTPException(status_code=422, detail="Invalid request payload: 'query' is required and must be non-empty")
    except Exception as exc:
        logger.exception("Failed to parse JSON payload for /query")
        raise HTTPException(status_code=400, detail="Malformed JSON body")

    query = data.query.strip()
    logger.info("Handling query", extra={"query_preview": query[:100]})

    try:
        routed = route_query(query)
        if not isinstance(routed, dict):
            logger.warning("Router returned non-dict result: %s", type(routed))
            routed = {"response": str(routed)}

        summary = summarize_output(routed)
        feedback = provide_feedback(summary)
        store_feedback(feedback)
        response_body = {"summary": summary, "feedback": feedback}
        return JSONResponse(response_body)
    except Exception:
        logger.exception("Error handling /query request")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/", response_class=HTMLResponse)
async def homepage():
    try:
        with open("frontend/templates/index.html") as f:
            return f.read()
    except FileNotFoundError:
        logger.error("index.html not found at frontend/templates/index.html")
        raise HTTPException(status_code=404, detail="Index page not found")


@app.get("/history", response_class=HTMLResponse)
async def history():
    try:
        with open("frontend/templates/history.html") as f:
            return f.read()
    except FileNotFoundError:
        logger.error("history.html not found at frontend/templates/history.html")
        raise HTTPException(status_code=404, detail="History page not found")

# For static files/assets: use Starlette, or uvicorn static mount in prod

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
