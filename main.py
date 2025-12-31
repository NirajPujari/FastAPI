from fastapi import FastAPI
from auth import router as auth_endpoints
from users import router as users_endpoints
from notes import router as notes_endpoints
from search import router as search_endpoints

app = FastAPI()

# Include authentication endpoints
app.include_router(auth_endpoints)

# Include users endpoints
app.include_router(users_endpoints, prefix="/users")

# Include notes endpoints
app.include_router(notes_endpoints, prefix="/notes")

# Include search endpoints
app.include_router(search_endpoints, prefix="/search")

@app.get("/")
def read_root():
    return {"Hello": "World"}