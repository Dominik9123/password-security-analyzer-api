from fastapi import FastAPI
from app.api.routes import router

# PL: Główna instancja aplikacji FastAPI z metadanymi widocznymi w Swagger UI.
# EN: Main FastAPI application instance with metadata displayed in Swagger UI.
app = FastAPI(
    title="Password Security Analyzer API",
    description="API for analyzing password strength and generating secure passwords.",
    version="1.0.0"
)

# PL: Wszystkie endpointy aplikacji są grupowane pod prefiksem /api.
# EN: All application endpoints are grouped under the /api prefix.
app.include_router(router, prefix="/api")
