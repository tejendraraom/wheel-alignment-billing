import logging
import os
from contextlib import asynccontextmanager

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text

from app.modules.customers.routes import router as customer_router
from app.modules.particulars.routes import router as particular_router
from app.modules.billing.routes import router as billing_router
from app.modules.technicians.routes import router as technician_router

logger = logging.getLogger(__name__)

_ALEMBIC_INI = os.path.join(os.path.dirname(__file__), "..", "alembic.ini")

# Arbitrary stable integer used as a PostgreSQL advisory lock ID.
# Ensures only one worker runs migrations at a time; others block and then
# proceed with a no-op `upgrade head` once the lock is released.
_MIGRATION_LOCK_ID = 741852963


def _run_migrations() -> None:
    alembic_cfg = Config(os.path.abspath(_ALEMBIC_INI))
    engine = create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)
    try:
        with engine.connect() as conn:
            logger.info("Acquiring migration advisory lock...")
            conn.execute(text(f"SELECT pg_advisory_lock({_MIGRATION_LOCK_ID})"))
            try:
                logger.info("Running Alembic migrations...")
                command.upgrade(alembic_cfg, "head")
                logger.info("Migrations complete.")
            finally:
                conn.execute(text(f"SELECT pg_advisory_unlock({_MIGRATION_LOCK_ID})"))
    finally:
        engine.dispose()


@asynccontextmanager
async def lifespan(app: FastAPI):
    _run_migrations()
    yield


app = FastAPI(
    title="Wheel Alignment Billing API",
    description="API for managing wheel alignment billing operations",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customer_router)
app.include_router(particular_router)
app.include_router(billing_router)
app.include_router(technician_router)


@app.get("/")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)