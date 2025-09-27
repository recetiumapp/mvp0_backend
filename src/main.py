# recetium backend/src/main.py
#
# Recetium MVP 0 
# Author: Rob Palencia / Sept.2025 
#
# Main FastAPI application entrypoint.
#

import uvicorn
from fastapi import FastAPI
from api.routes import users, alley
from db.session import init_db

app = FastAPI(title="Recetium API - MVP 0")

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(users.router)
app.include_router(alley.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
