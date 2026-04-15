✅ Microservice 1: Inventory Service
📦 Purpose

Manages product stock
Responds to availability checks
Updates inventory when an order is placed


📁 Folder Structure
inventory-service/
│── app/
│   ├── main.py
│── requirements.txt
│── Dockerfile


🧠 main.py
Pythonfrom fastapi import FastAPI, HTTPExceptionfrom pydantic import BaseModelapp = FastAPI(title="Inventory Service")# In-memory inventory (for demo)inventory_db = {    "P1001": 10,    "P1002": 5}class InventoryResponse(BaseModel):    product_id: str    available_quantity: int@app.get("/inventory/{product_id}", response_model=InventoryResponse)def check_inventory(product_id: str):    if product_id not in inventory_db:        raise HTTPException(status_code=404, detail="Product not found")    return {        "product_id": product_id,        "available_quantity": inventory_db[product_id]    }@app.put("/inventory/{product_id}")def update_inventory(product_id: str, quantity: int):    if product_id not in inventory_db:        raise HTTPException(status_code=404, detail="Product not found")    if inventory_db[product_id] < quantity:        raise HTTPException(status_code=400, detail="Insufficient stock")    inventory_db[product_id] -= quantity    return {"message": "Inventory updated successfully"}Show more lines

📦 requirements.txt
Plain TextfastapiuvicornShow more lines

🐳 Dockerfile
DockerfileFROM python:3.10-slimWORKDIR /appCOPY requirements.txt .RUN pip install --no-cache-dir -r requirements.txtCOPY app appCMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081"]Show more lines

✅ Microservice 2: Order Service
📦 Purpose

Accepts customer orders
Calls Inventory Service before confirming order


📁 Folder Structure
order-service/
│── app/
│   ├── main.py
│── requirements.txt
│── Dockerfile


🧠 main.py
Pythonfrom fastapi import FastAPI, HTTPExceptionfrom pydantic import BaseModelimport requestsimport uuidapp = FastAPI(title="Order Service")INVENTORY_SERVICE_URL = "http://inventory-service:8081"orders_db = {}class OrderRequest(BaseModel):    product_id: str    quantity: int@app.post("/orders")def create_order(order: OrderRequest):    inventory_url = f"{INVENTORY_SERVICE_URL}/inventory/{order.product_id}"    response = requests.get(inventory_url)    if response.status_code != 200:        raise HTTPException(status_code=400, detail="Product not available")    available_qty = response.json()["available_quantity"]    if order.quantity > available_qty:        raise HTTPException(status_code=400, detail="Insufficient inventory")    # Update inventory    update_resp = requests.put(        inventory_url,        params={"quantity": order.quantity}    )    if update_resp.status_code != 200:        raise HTTPException(status_code=400, detail="Failed to update inventory")    order_id = str(uuid.uuid4())    orders_db[order_id] = order.dict()    return {        "order_id": order_id,        "status": "Order confirmed"    }@app.get("/orders/{order_id}")def get_order(order_id: str):    if order_id not in orders_db:        raise HTTPException(status_code=404, detail="Order not found")    return orders_db[order_id]``Show more lines

📦 requirements.txt
Plain TextfastapiuvicornrequestsShow more lines

🐳 Dockerfile
DockerfileFROM python:3.10-slimWORKDIR /appCOPY requirements.txt .RUN pip install --no-cache-dir -r requirements.txtCOPY app appCMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]Show more lines

