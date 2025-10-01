# recetium_backend/src/main.py
#
# Recetium MVP 0 
# Author: Rob Palencia / Sept.2025 
#
# Main FastAPI application entrypoint.
#

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import users, alley
from db.session import init_db

app = FastAPI(title="Recetium API - MVP 0")

# CORS configuration
origins = [
    "http://127.0.0.1:8001",  # frontend local
    "http://localhost:8001",  # frontend local con localhost
    "http://app.recetium.com",  # frontend 
    "https://recetium-frontend.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],          # permite todos los métodos (GET, POST, PUT, DELETE...)
    allow_headers=["*"],          # permite todos los headers
)

@app.on_event("startup")
async def startup():
    await init_db()

# Routers 
app.include_router(users.router)
app.include_router(alley.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
