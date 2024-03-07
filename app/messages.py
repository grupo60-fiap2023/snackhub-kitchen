import boto3
import json
import os
from app.schemas import StatusPedidoSchema
from app.models import StatusPedido
from datetime import datetime
from app.database import get_db

sqs = boto3.client('sqs', region_name=os.environ.get("REGION"), aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

fila_order_succeeded = sqs.get_queue_url(QueueName='order_succeeded.fifo')['QueueUrl']
fila_order_status = sqs.get_queue_url(QueueName='order-status.fifo')['QueueUrl']

def enviar_mensagem_saida(mensagem):
    print(sqs.send_message(
        QueueUrl=fila_order_status,
        MessageBody=json.dumps(mensagem),
        MessageGroupId='112',
        MessageDeduplicationId = '112'))

def processar_mensagens_entrada():
    while True:
        response = sqs.receive_message(
            QueueUrl = fila_order_succeeded,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20
        )

        if 'Messages' in response:
            for message in response['Messages']:
                corpo_mensagem = json.loads(message['Body'])
                reg = StatusPedidoSchema()

                reg.id = corpo_mensagem['order-id']
                reg.numeropedido = corpo_mensagem['ticket-number']
                reg.timestamp = datetime.utcnow()
                reg.updatedAt = datetime.utcnow()
                reg.status = 1
                reg.itens = ", ".join(corpo_mensagem['itens'])
                
                db = next(get_db())
                try:
                    novo_status_pedido = StatusPedido(**reg.dict())
                    db.add(novo_status_pedido)
                    db.commit()
                except Exception as e:
                    print(e)
                finally:
                    db.close()

                sqs.delete_message(
                    QueueUrl=fila_order_succeeded,
                    ReceiptHandle=message['ReceiptHandle']
                )

