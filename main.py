from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from typing import Optional

# --- Configuration ---
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1px0OQ1fIDULtfreJ7XMBNOjooKQXu8wZP73FOuHDjJc'  # Replace with your Google Sheet ID
RANGE_NAME = 'Sheet1!A1:O'  # Adjust sheet name if needed
CREDENTIALS_FILE = 'credentials.json'

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Google Sheets service
def get_sheets_service():
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service

# Check if PR number exists
def is_pr_number_duplicate(pr_number: str) -> bool:
    service = get_sheets_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute()
    rows = result.get('values', [])

    # Skip header
    for row in rows[1:]:
        if len(row) > 1 and row[1].strip() == pr_number.strip():  # PR Number is 2nd column (index 1)
            return True
    return False

# Append new row
def append_to_sheet(data: list):
    service = get_sheets_service()
    body = {'values': [data]}
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        body=body
    ).execute()

# Request model
class InventoryItem(BaseModel):
    system: str
    pr_number: str
    po_number: str
    project_code: str
    plant_code: str
    drsc: str
    model_no: str
    make: str
    order_qty: str
    on_hand_qty: str
    in_store_avail: str
    received_qty: str
    remarks: Optional[str] = None
    stock_location: str

# Routes
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit")
async def submit_form(item: InventoryItem):
    if is_pr_number_duplicate(item.pr_number):
        raise HTTPException(status_code=400, detail="PR Number must be unique.")

    data = [
        item.system,
        item.pr_number,
        item.po_number,
        item.project_code,
        item.plant_code,
        item.drsc,
        item.model_no,
        item.make,
        item.order_qty,
        item.on_hand_qty,
        item.in_store_avail,
        item.received_qty,
        item.remarks or "",  # Handle None for remarks
        item.stock_location
    ]
    try:
        append_to_sheet(data)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
