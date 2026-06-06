from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# A mock database to store our items
inventory = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Smartphone", "price": 499.99},
]

class Item(BaseModel):
    id: int
    name: str
    price: float

@app.get('/')
def welcome():
    return {'message': 'Welcome to my FastAPI application'}

@app.get('/inventory')
async def getAll():
    return inventory

@app.post('/inventory')
async def addItem(item: Item):
    inventory.append(item.model_dump())
    return inventory

@app.put('/inventory/{id}')
async def update_item(id: int, item:Item):
    for index, existing_item in enumerate(inventory):
        if existing_item["id"] == id:
            inventory[index] = item.model_dump()
            return inventory[index]
    raise HTTPException(status_code=404, detail='item not found')

@app.delete('/inventory/{id}')
async def delete(id: int):
    for index, item in enumerate(inventory):
        if item["id"] == id:
            del inventory[index]
            return {"message": "Item deleted"}

    raise HTTPException(status_code=404, detail="Item not found")