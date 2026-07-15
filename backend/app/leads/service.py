import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.config import settings
from app.leads.models import Lead
from app.leads.scoring import LeadScoringEngine

class LeadService:
    @staticmethod
    async def get_lead_by_id(db: AsyncSession, lead_id: int) -> Lead | None:
        result = await db.execute(select(Lead).filter(Lead.id == lead_id))
        return result.scalars().first()

    @staticmethod
    async def get_all_leads(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Lead]:
        result = await db.execute(select(Lead).offset(skip).limit(limit).order_by(Lead.opportunity_score.desc()))
        return list(result.scalars().all())

    @staticmethod
    async def process_and_create_lead(db: AsyncSession, company_name: str, website_url: str, data_payload: dict) -> Lead:
        # 1. Pipeline Layer: Calculate Custom Heuristic Score
        scoring_engine = LeadScoringEngine(data_payload)
        calculated_score = scoring_engine.calculate_opportunity_score()

        # 2. Pipeline Layer: Call LLM API (Gemini) Wrapper via Async HTTP
        generated_hook = await LeadService._generate_llm_outreach(
            company_name=company_name,
            score=calculated_score,
            metrics=data_payload
        )

        # 3. Database Persistence Layer
        db_lead = Lead(
            company_name=company_name,
            website_url=website_url,
            data_payload=data_payload,
            opportunity_score=calculated_score,
            conversion_status="NEW",
            generated_outreach=generated_hook
        )
        
        db.add(db_lead)
        await db.commit()
        await db.refresh(db_lead)
        return db_lead

    @staticmethod
    async def _generate_llm_outreach(company_name: str, score: int, metrics: dict) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        
        # Frame granular performance issues explicitly
        prompt = (
            f"Write a short, professional, 2-sentence B2B email hook for {company_name}. "
            f"Their website has an optimization pain rating of {score}/100. "
            f"Specific diagnostics: Page load speed is {metrics.get('page_load_speed_seconds')}s, "
            f"Mobile Responsive status: {metrics.get('is_mobile_responsive')}. "
            f"Do not use generic buzzwords. Address the functional gaps directly, highlighting optimization opportunities."
        )

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 150
            }
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    return data["candidates"][0]["content"]["parts"][0]["text"].strip()
                else:
                    return f"Hello {company_name}, we noticed technical optimization gaps on your site that are impacting your customer experience."
        except Exception:
            return f"Hello {company_name}, we noticed technical optimization gaps on your site that are impacting your customer experience."