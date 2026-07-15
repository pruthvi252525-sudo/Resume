import datetime
from typing import Any, Dict
from sqlalchemy import BigInteger, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, autoincrement=True)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    website_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    
    # Structured payload storing scraped performance indicators
    data_payload: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    
    # Analytics & Scoring metrics
    opportunity_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    conversion_status: Mapped[str] = mapped_column(String(50), nullable=False, default="NEW", index=True)
    
    # Generative AI Outreach Hooks
    generated_outreach: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Audit Trail Columns
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )