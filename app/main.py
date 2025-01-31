import os

import uvicorn
from api.routes import router
from fastapi import FastAPI

app = FastAPI()

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.getenv("PORT", 8000))