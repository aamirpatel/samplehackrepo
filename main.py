#Inventory Service
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Inventory Service")

# In-memory inventory (for demo)
inventory_db = {
    "P1001": 10,
    "P1002": 5
}

class InventoryResponse(BaseModel):
    product_id: str
    available_quantity: int

@app.get("/inventory/{product_id}", response_model=InventoryResponse)
def check_inventory(product_id: str):
    if product_id not in inventory_db:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "product_id": product_id,
        "available_quantity": inventory_db[product_id]
    }

@app.put("/inventory/{product_id}")
def update_inventory(product_id: str, quantity: int):
    if product_id not in inventory_db:
        raise HTTPException(status_code=404, detail="Product not found")

    if inventory_db[product_id] < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    inventory_db[product_id] -= quantity
    return {"message": "Inventory updated successfully"}
