from app.database import engine, Base
from app.models import user 
from fastapi import FastAPI
from app.models import stress
from app.api import stress

app=FastAPI()
app.include_router(stress.router)
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
	return {"message":"MindEase AI Backend Running"}
