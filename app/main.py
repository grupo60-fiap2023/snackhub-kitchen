from fastapi.middleware.cors import CORSMiddleware
from app import models, pedidos
from app.database import engine
from fastapi import FastAPI
import boto3
import threading
from queue_consumer import receive_messages
from moto import mock_sqs

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


aws_access_key_id = ''
aws_secret_access_key = ''
region_name = ''

with mock_sqs():
    sqs = boto3.client('sqs', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    queue_url = 'order_success'

    thread = threading.Thread(target = receive_messages, args=(sqs, queue_url))
    thread.daemon = True
    thread.start()