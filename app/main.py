from fastapi import FastAPI
from app.api.routes import router as api_router
from app.models.database import Base, engine
from app.models import tables

Base.metadata.create_all(bind=engine)

app = FastAPI(title="VirusTotal Data Pipeline")
app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Welcome to the VirusTotal API Wrapper"}