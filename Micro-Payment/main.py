from typing import Union
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pymongo import MongoClient
import requests

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#connect to mongodb
mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["micro-payment"]
collection = db["products"] #collection name

# Base URL of the Product Service
PRODUCT_SERVICE_URL = "http://localhost:8000/products"

# Endpoint to create an order
@app.post("/orders")   #create order 
def create_order(product_id: str, quantity: int):
    # Fetch product details from the Product Service
    product_response = requests.get(f"{PRODUCT_SERVICE_URL}/{product_id}")
    
    if product_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = product_response.json()
    
    # Check if the requested quantity is available
    if product["quantity"] < quantity:
        raise HTTPException(status_code=400, detail="Insufficient quantity available")
    
    # Calculate the total price
    total_price = product["price"] * quantity
    
    # Create the order
    order = {
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity,
        "total_price": product["price"] * quantity
    }
    
    # Save the order to MongoDB
    collection.insert_one(order)
    
    #we need to update the product quantity in the product service
    update_product_response = requests.put(f"{PRODUCT_SERVICE_URL}/{product_id}", json={"quantity": product["quantity"] - quantity})
    
    if update_product_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to update product quantity in Product Service")
    
    # Return the order details
    return {"message": "Order created successfully", "order": order}

@app.get("/orders")
def get_all_orders():
    return list(collection.find())

#we will provide the port for the microservice
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
        
