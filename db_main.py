from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os

# Import DB modules
from database import SessionLocal, engine
from models import Base, InventoryItem

# Create DB folder and tables
os.makedirs("data", exist_ok=True)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for request
class InventoryCreate(BaseModel):
    system: str
    pr_number: str
    po_number: str
    project_code: str
    plant_code: str
    drsc: str
    model_no: str
    make: str
    order_quantity: str
    on_hand_quantity: str
    in_store_availability: str
    received_qty: str
    remarks: str
    stock_location: str

# Routes
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit")
async def submit_form(item: InventoryCreate, db: Session = Depends(get_db)):
    # Check if PR number already exists
    existing = db.query(InventoryItem).filter(InventoryItem.pr_number == item.pr_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="PR Number must be unique.")

    # Save to DB
    db_item = InventoryItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return {"success": True, "id": db_item.id}