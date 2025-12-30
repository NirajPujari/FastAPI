from fastapi import FastAPI
from auth import router as auth_endpoints
from notes import router as notes_endpoints
from search import router as search_endpoints

app = FastAPI()

# Include authentication endpoints
app.include_router(auth_endpoints)

# Include note endpoints
app.include_router(notes_endpoints, prefix="/notes")

# Include api endpoints
app.include_router(search_endpoints, prefix="/search")

@app.get("/")
def read_root():
    return {"Hello": "World"}