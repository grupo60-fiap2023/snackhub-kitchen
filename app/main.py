from fastapi.middleware.cors import CORSMiddleware
from app import models, pedidos
from app.database import engine
from fastapi import FastAPI

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pedidos.router, tags=["Kitchen"], prefix="/kitchen")

@app.get("/api/healthchecker")
def root():
    return {"message": "The API is LIVE!!"}