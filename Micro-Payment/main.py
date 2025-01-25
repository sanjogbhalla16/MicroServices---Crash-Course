from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from redis_om import get_redis_connection,HashModel
from starlette.requests import Request
import requests
import uvicorn
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

redis = get_redis_connection(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)

# now we make the orders
class Order(HashModel):
    product_id: str
    price: float
    fee: str
    total: float
    quantity: int
    status: str # pending, completed or failed

    class Config:
        database = redis

@app.post("/orders")
async def create_order(request: Request): #id and quantity
    body = await request.json()
    
    #we are getting this product from another microservice so we use requests
    request = requests.get("http://localhost:8000/products/%s" % body["id"])
    # product = request.json()
    # order = Order(
    #     product_id=body["id"],
    #     quantity=body["quantity"],
    #     price=product["price"],
    #     fee=0.2 * product["price"],
    #     total=1.2 * product["price"]
    # )
    # order.save()
    return request.json()