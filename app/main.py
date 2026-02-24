from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from alembic import command
from alembic.config import Config
import os

from app.core.database import engine, Base
from app.models.customer import Customer  # noqa
from app.modules.customers.routes import router as customer_router
from app.models.particular import Particular  # noqa
from app.modules.particulars.routes import router as particular_router
from app.models.bill import Bill  # noqa
from app.models.bill_item import BillItem  # noqa
from app.modules.billing.routes import router as billing_router
from app.models.technician import Technician  # noqa
from app.modules.technicians.routes import router as technician_router


app = FastAPI(
    title="Wheel Alignment Billing API",
    description="API for managing wheel alignment billing operations",
    version="1.0.0"
)

# Configure CORS
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

@app.on_event("startup")
def startup():
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
    command.upgrade(alembic_cfg, "head")

@app.get("/")
def health():
    return {"status": "ok"}

# @app.get("/")
# async def root():
#     return {
#         "message": "Welcome to Wheel Alignment Billing API",
#         "status": "running",
#         "version": "1.0.0"
#     }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)