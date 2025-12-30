from fastapi import FastAPI
from auth import router as auth_endpoints
# from search import endpoints as search_endpoints
# from notes import endpoints as notes_endpoints

app = FastAPI()

# # Include api endpoints
# app.include_router(search_endpoints.router, prefix="/api")

# # Include note endpoints
# app.include_router(notes_endpoints.router, prefix="/api/notes")

# Include authentication endpoints
app.include_router(auth_endpoints)

@app.get("/")
def read_root():
    return {"Hello": "World"}