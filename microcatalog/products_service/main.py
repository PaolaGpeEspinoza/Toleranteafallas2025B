from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import json
import os
import requests

AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL")


app = FastAPI(title="ProductService - Microcatalog")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Product(BaseModel):
    name: str
    price: float

api_key_scheme = APIKeyHeader(name="Authorization")

def verify_token(api_key: str = Depends(api_key_scheme)):
    if api_key.startswith("Bearer "):
        token = api_key.replace("Bearer ", "")
    else:
        token = api_key
    try:
        response = requests.get(
            AUTH_SERVICE_URL,
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise HTTPException(status_code=401, detail="Token inválido")
        else:
            raise HTTPException(status_code=500, detail="Error conectando con AuthService")
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="Error conectando con AuthService")

PRODUCTS_FILE = "products.json"

def load_products():
    if not os.path.exists(PRODUCTS_FILE):
        return []
    with open(PRODUCTS_FILE, "r") as f:
        return json.load(f)

def save_products(products):
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f, indent=4)

@app.get("/products", response_model=list[Product])
def get_products():
    return load_products()

@app.post("/products/add")
def add_product(product: Product, token_data: dict = Depends(verify_token)):
    products = load_products()
    products.append(product.dict())
    save_products(products)
    return {"message": "Producto agregado", "added_by": token_data["user"]}

@app.delete("/products/delete/{index}")
def delete_product(index: int, token_data: dict = Depends(verify_token)):
    products = load_products()
    if index < 0 or index >= len(products):
        raise HTTPException(status_code=400, detail="Índice inválido")

    deleted = products.pop(index)
    save_products(products)
    return {"message": "Producto eliminado", "deleted": deleted, "deleted_by": token_data["user"]}
