#Inventory Service

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Inventory Service")

# In-memory inventory
inventory = {
    "P1001": 10,
    "P1002": 5,
    "P1003": 20
}

@app.get("/inventory/{product_id}")
def get_inventory(product_id: str):
    if product_id not in inventory:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "product_id": product_id,
        "available_quantity": inventory[product_id]
    }

@app.put("/inventory/{product_id}")
def reduce_inventory(product_id: str, quantity: int):
    if product_id not in inventory:
        raise HTTPException(status_code=404, detail="Product not found")

    if inventory[product_id] < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    inventory[product_id] -= quantity
    return {"message": "Inventory updated"}
``
