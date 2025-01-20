from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

redis = get_redis_connection(
    host="redis-11455.c16.us-east-1-3.ec2.redns.redis-cloud.com",
    port=11455,
    password="ywV3wyoyawqmv749vAqxQWoi5uFjU7et",
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int
    
    class Meta:
        database = redis
    
    class Config:
        arbitrary_types_allowed = True

@app.get("/products")
def all():
    return Product.all_pks()

@app.post("/products")
def create_product(product: Product):
    return product.save()