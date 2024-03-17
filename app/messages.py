import boto3
import json
import os
from app.schemas import StatusPedidoSchema
from app.models import StatusPedido
from datetime import datetime
from app.database import get_db

sqs = boto3.client('sqs', region_name=os.environ.get("REGION"), aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

fila_order_succeeded = sqs.get_queue_url(QueueName='order-successful-topic')['QueueUrl']
fila_order_status = sqs.get_queue_url(QueueName='order-status-topic')['QueueUrl']

def enviar_mensagem_saida(mensagem):
    print(sqs.send_message(
        QueueUrl=fila_order_status,
        MessageBody=json.dumps(mensagem)))

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

                reg.id = corpo_mensagem['orderId']
                reg.numeropedido = corpo_mensagem['orderIdentifier']
                reg.timestamp = datetime.utcnow()
                reg.updatedAt = datetime.utcnow()
                reg.status = 5
                reg.itens = json.dumps(corpo_mensagem['itens'])
                
                db = next(get_db())
                try:
                    novo_status_pedido = StatusPedido(**reg.dict())
                    db.add(novo_status_pedido)
                    db.commit()
                    print("Deu bom!")
                except Exception as e:
                    print(e)
                finally:
                    db.close()

                sqs.delete_message(
                    QueueUrl=fila_order_succeeded,
                    ReceiptHandle=message['ReceiptHandle']
                )

