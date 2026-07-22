from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.api.v1 import auth, projects, tickets

app = FastAPI(title="Project Tracker API", version="1.0.0", description="Mini-Jira project and ticket management API")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(tickets.router, prefix="/api/v1")
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", include_in_schema=False)
async def demo():
    return FileResponse(static_dir / "index.html")


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
