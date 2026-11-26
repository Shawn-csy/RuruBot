import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()  # 必須在 adapter import 之前，adapter 建構時需要 env var

from api.routes import router as api_router
from middlewares.rate_limit import ApiRateLimitMiddleware
from services.adapters.line_webhook import get_handler, callback

app = FastAPI()
cors_origins = os.environ.get("CORS_ALLOW_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in cors_origins],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ApiRateLimitMiddleware)
app.include_router(api_router)

FRONTEND_DIST = Path(__file__).parent / "frontend" / "dist"
if (FRONTEND_DIST / "assets").is_dir():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")
if (FRONTEND_DIST / "pixel-worlds").is_dir():
    app.mount(
        "/pixel-worlds",
        StaticFiles(directory=FRONTEND_DIST / "pixel-worlds"),
        name="pixel-worlds",
    )
if (FRONTEND_DIST / "images").is_dir():
    app.mount(
        "/images",
        StaticFiles(directory=FRONTEND_DIST / "images"),
        name="images",
    )


@app.get("/")
@app.get("/about")
@app.get("/guide")
def read_root():
    index_file = FRONTEND_DIST / "index.html"
    if index_file.is_file():
        return FileResponse(index_file)
    return {"message": "Hello, World!"}


@app.get("/favicon.ico", include_in_schema=False)
@app.get("/favicon-32x32.png", include_in_schema=False)
@app.get("/apple-touch-icon.png", include_in_schema=False)
@app.get("/robots.txt", include_in_schema=False)
@app.get("/sitemap.xml", include_in_schema=False)
def read_public_root_file(request: Request):
    filename = request.url.path.lstrip("/")
    target = FRONTEND_DIST / filename
    if target.is_file():
        return FileResponse(target)
    raise HTTPException(status_code=404, detail="Not found")


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    required_env = ("CHANNEL_SECRET", "CHANNEL_ACCESS_TOKEN")
    missing_env = [name for name in required_env if not os.getenv(name)]
    ticket_data_path = os.path.join(os.path.dirname(__file__), "statics", "light_grass_poem.json")
    checks = {
        "env": not missing_env,
        "ticket_data": os.path.exists(ticket_data_path),
    }
    status = "ok" if all(checks.values()) else "degraded"
    return {
        "status": status,
        "checks": checks,
        "missing_env": missing_env,
    }


app.post("/callback")(callback)

# 觸發 handler 建立（確保 @handler.add 事件已註冊）
get_handler()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
