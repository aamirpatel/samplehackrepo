#Microservice 2: Order Service

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import uuid

app = FastAPI(title="Order Service")

INVENTORY_SERVICE_URL = "http://inventory-service:8081"

orders_db = {}

class OrderRequest(BaseModel):
    product_id: str
    quantity: int

@app.post("/orders")
def create_order(order: OrderRequest):
    inventory_url = f"{INVENTORY_SERVICE_URL}/inventory/{order.product_id}"

    response = requests.get(inventory_url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Product not available")

    available_qty = response.json()["available_quantity"]
    if order.quantity > available_qty:
        raise HTTPException(status_code=400, detail="Insufficient inventory")

    # Update inventory
    update_resp = requests.put(
        inventory_url,
        params={"quantity": order.quantity}
    )
    if update_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to update inventory")

    order_id = str(uuid.uuid4())
    orders_db[order_id] = order.dict()

    return {
        "order_id": order_id,
        "status": "Order confirmed"
    }

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")

    return orders_db[order_id]
``
