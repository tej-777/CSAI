from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from agents.routeragent import route_query
from agents.summarizeragent import summarize_output
from agents.criticagent import provide_feedback
from agents.feedbackmanager import store_feedback
from database.dbmanager import DatabaseManager
from config import settings

app = FastAPI()
db = DatabaseManager()


@app.post("/query")
async def handle_query(request: Request):
    data = await request.json()
    query = data.get("query", "")
    routed = route_query(query)
    summary = summarize_output(routed)
    feedback = provide_feedback(summary)
    store_feedback(feedback)
    return JSONResponse({"summary": summary, "feedback": feedback})


@app.get("/", response_class=HTMLResponse)
async def homepage():
    with open("frontend/templates/index.html") as f:
        return f.read()


@app.get("/history", response_class=HTMLResponse)
async def history():
    with open("frontend/templates/history.html") as f:
        return f.read()

# For static files/assets: use Starlette, or uvicorn static mount in prod

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
