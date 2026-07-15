from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.leads.service import LeadService

router = APIRouter(prefix="/leads", tags=["leads"])

# --- API Pydantic Schemas ---
class DataPayloadSchema(BaseModel):
    page_load_speed_seconds: float
    is_mobile_responsive: bool
    tracking_pixels: List[str]

class LeadCreateRequest(BaseModel):
    company_name: str
    website_url: HttpUrl
    data_payload: DataPayloadSchema

class LeadResponseSchema(BaseModel):
    id: int
    company_name: str
    website_url: str
    data_payload: dict
    opportunity_score: int
    conversion_status: str
    generated_outreach: Optional[str]

    class Config:
        from_attributes = True

# --- API Core Endpoints ---
@router.post("/", response_model=LeadResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_lead(payload: LeadCreateRequest, db: AsyncSession = Depends(get_db)):
    try:
        lead = await LeadService.process_and_create_lead(
            db=db,
            company_name=payload.company_name,
            website_url=str(payload.website_url),
            data_payload=payload.data_payload.model_dump()
        )
        return lead
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline processing failed: {str(e)}")

@router.get("/", response_model=List[LeadResponseSchema])
async def read_leads(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    leads = await LeadService.get_all_leads(db=db, skip=skip, limit=limit)
    return leads

@router.get("/{lead_id}", response_model=LeadResponseSchema)
async def read_lead(lead_id: int, db: AsyncSession = Depends(get_db)):
    lead = await LeadService.get_lead_by_id(db=db, lead_id=lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Requested Lead resource not found")
    return lead