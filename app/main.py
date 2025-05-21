from fastapi import FastAPI
from app.api.routes import router
from app.tasks.ingest import ingest_all_data
from app.models.database import create_tables

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
def startup_event():
    create_tables()
    ingest_all_data()  # Optional: you can control this via env/flag
