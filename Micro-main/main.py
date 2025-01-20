from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from dotenv import load_dotenv
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

class Product(HashModel):
    name: str
    price: float
    quantity: int
    
    class Meta:
        database = redis
    
    class Config:
        arbitrary_types_allowed = True
    
    def model_dump(self, **kwargs):
        # Use this if ExpressionProxy fields are present and should be excluded
        return super().model_dump(**kwargs)

@app.get("/products")
def all():
    return Product.all_pks()

@app.post("/products")
def create_product(product: Product):
    return product.save()