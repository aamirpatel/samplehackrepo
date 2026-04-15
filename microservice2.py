#Microservice 2: Order Service

from fastapi import FastAPI, HTTPException
import requests
import uuid

app = FastAPI(title="Order Service")

INVENTORY_SERVICE_URL = "http://inventory-service:8081"

# In-memory orders
orders = {}

@app.post("/orders")
def create_order(product_id: str, quantity: int):

    # Check inventory
    inventory_api = f"{INVENTORY_SERVICE_URL}/inventory/{product_id}"
    response = requests.get(inventory_api)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Product unavailable")

    if quantity > response.json()["available_quantity"]:
        raise HTTPException(status_code=400, detail="Not enough stock")

    # Reduce inventory
    reduce_resp = requests.put(inventory_api, params={"quantity": quantity})
    if reduce_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Inventory update failed")

    order_id = str(uuid.uuid4())
    orders[order_id] = {
        "product_id": product_id,
        "quantity": quantity,
        "status": "CONFIRMED"
    }

    return {"order_id": order_id, "status": "Order confirmed"}

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders[order_id]
``
