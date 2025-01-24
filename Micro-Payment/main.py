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
PRODUCT_SERVICE_URL = os.getenv("REDIS_URI")

# Endpoint to create an order
@app.post("/orders")   #all products
def create_order(product_id: str, quantity: int):
    # Fetch product details from the Product Service
    product_response = requests.get(f"{PRODUCT_SERVICE_URL}/{product_id}")
    
    if product_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = product_response.json()
    
    # Calculate the total price
    total_price = product["price"] * quantity
    
    # Create the order
    order = {
        "product_id": product_id,
        "quantity": quantity,
        "total_price": total_price
    }
    
    # Save the order to MongoDB
    collection.insert_one(order)
    
    return {"message": "Order created successfully"}
        
