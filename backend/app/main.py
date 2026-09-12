"""FastAPI application entry point for VERIFY GH."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database.connection import engine
from app.routes import auth, dashboard, products, reports, verifications

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    yield
    # Shutdown
    engine.dispose()


app = FastAPI(
    title=settings.app_name,
    description="VERIFY GH - Consumer Product Verification and Regulatory Reporting Platform for Ghana",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(verifications.router)
app.include_router(reports.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "description": "VERIFY GH - Check it. Match it. Trust the information.",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": settings.app_name}
