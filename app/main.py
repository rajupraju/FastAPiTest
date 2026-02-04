from fastapi import FastAPI, Request
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import uuid


dev = FastAPI()

@dev.get("/")
def root():
    return {"message": "Inner FastAPI with Docker Compose pushed from local 🚀"}

@dev.get("/health")
def health():
    return {"status": "Inner healthy pushed from local"}


# In-memory database (for demonstration purposes)
items = []

# Pydantic model for item data
class Item(BaseModel):
    name: str
    description: str

# Create an item
@dev.post("/items/", response_model=Item)
async def create_item(item: Item):
    items.append(item)
    return item

@dev.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

# Update an item
@dev.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    
    items[item_id] = item
    return item

# Delete an item
@dev.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    
    deleted_item = items.pop(item_id)
    return deleted_item

dev.mount("/statics",StaticFiles(directory="app/statics"),name="statics")
templates=Jinja2Templates(directory="app/templatess")

dev.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key"
)

@dev.get("/html",response_class=HTMLResponse)
async def give_html(request: Request):
    name =request.session.get("name")
    if name:
     return templates.TemplateResponse("index.html",{"request": request,"name": name})
    else:
     return """ <h2>Please signup fisrt</h2>"""

@dev.get("/html/{names}",response_class=HTMLResponse)
async def give_html(request: Request,names : str):
    request.session["id"]=str(uuid.uuid4())
    request.session["name"]=names
    return """<h2>signup completed</h2>"""
