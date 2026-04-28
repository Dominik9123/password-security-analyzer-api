from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router


app = FastAPI(
    title="Password Security Analyzer API",
    description="API for analyzing password strength and generating secure passwords.",
    version="1.0.0"
)

# PL: CORS pozwala frontendowi z osobnego adresu/Live Servera laczyc sie z API.
# EN: CORS lets the frontend served from Live Server call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PL: Wszystkie endpointy aplikacji sa dostepne pod wspolnym prefiksem /api.
# EN: All application endpoints are grouped under the shared /api prefix.
app.include_router(router, prefix="/api")
