from sqlalchemy import Column, String, Integer, Text
from database import Base

class InventoryItem(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    system = Column(String(100))
    pr_number = Column(String(100), unique=True, index=True)  # Must be unique
    po_number = Column(String(100))
    project_code = Column(String(100))
    plant_code = Column(String(50))
    drsc = Column(String(100))
    model_no = Column(String(100))
    make = Column(String(100))
    order_quantity = Column(String(50))
    on_hand_quantity = Column(String(50))
    in_store_availability = Column(String(50))
    received_qty = Column(String(50))
    remarks = Column(Text)
    stock_location = Column(String(200))