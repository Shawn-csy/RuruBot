import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()  # 必須在 adapter import 之前，adapter 建構時需要 env var

from api.routes import router as api_router
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
app.include_router(api_router)

app.get("/")(lambda: {"message": "Hello, World!"})


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
