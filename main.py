import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()  # 必須在 adapter import 之前，adapter 建構時需要 env var

from api.routes import router as api_router
from services.adapters.line_webhook import get_handler, callback

app = FastAPI()
app.include_router(api_router)

app.get("/")(lambda: {"message": "Hello, World!"})
app.post("/callback")(callback)

# 觸發 handler 建立（確保 @handler.add 事件已註冊）
get_handler()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
