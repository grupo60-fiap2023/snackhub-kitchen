import time
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import get_db

def receive_messages(sqs, queue_url, db: Session = Depends(get_db)):
    
    while True:
        try:
            response = sqs.receive_messages(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
                VisibilityTimeout = 10
            )

            messages = response.get('Messages',[])
            for message in messages:
                sqs.delete_message(
                    QueueUrl = queue_url,
                    ReceiptHandle = message['ReceiptHandle']
                )
        except Exception as e:
            print("Ocorreu um erro:", e)

        time.sleep(1)

