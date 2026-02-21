from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import user, stress  # Keep models together
from app.api.stress import router as stress_router # Alias the router!
from app.api.user import router as user_router

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all frontends (good for local development) 
    allow_credentials=True,
    allow_methods=["*"], # Allows POST, GET, etc.
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Include the aliased router
app.include_router(stress_router)
app.include_router(user_router)  #Added user router

@app.get("/")
def root():
    return {"message": "MindEase AI Backend Running"}
