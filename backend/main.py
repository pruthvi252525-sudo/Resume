from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.leads.router import router as leads_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS so your Next.js frontend can talk to the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the leads pipeline routes
app.include_router(leads_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"status": "online", "message": "B2B Lead Acquisition Engine Live"}