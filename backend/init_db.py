# backend/init_db.py
import asyncio
import sys
import os

# Ensure the backend directory is in the system path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base
from app.leads.models import Lead  # Import registers the Lead table model

async def create_tables():
    print("⏳ Connecting to PostgreSQL and initializing schema layouts...")
    try:
        async with engine.begin() as conn:
            # Drop existing tables if you want a clean reset, otherwise leave commented
            # await conn.run_sync(Base.metadata.drop_all)
            
            # Creates all tables defined by SQLAlchemy models
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables successfully created within lead_db context!")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("\n💡 Pro-Tip: Ensure your PostgreSQL service is running and the database 'lead_db' exists.")

if __name__ == "__main__":
    asyncio.run(create_tables())