from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

app = FastAPI(
    title="Password Security Analyzer API",
    description="API for analyzing password strength and generating secure passwords.",
    version="1.0.0"
)

# Allow the local frontend to call the API while it is served separately.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Keep all application routes under one shared API prefix.
app.include_router(router, prefix="/api")
