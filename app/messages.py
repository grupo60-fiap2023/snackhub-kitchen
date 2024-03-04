# import boto3
# import json

# sqs = boto3.client('sqs', region_name=os.environ.get("REGION"))

# fila_order_succeeded = sqs.get_queue_url(QueueName='order_succeeded')['QueueUrl']
# fila_order_status = sqs.get_queue_url(QueueName='order-status')['QueueUrl']

# def enviar_mensagem_saida(mensagem):
#     sqs.send_message(QueueUrl=fila_order_status, MessageBody=json.dumps(mensagem))

# def processar_mensagens_entrada():
#     while True:
#         response = sqs.receive_message(
#             QueueUrl = fila_order_succeeded,
#             MaxNumberOfMessages=1,
#             WaitTimeSeconds=20
#         )

#         if 'Messages' in response:
#             for message in response['Message']:
#                 corpo_mensagem = json.loads(message['Body'])

#                 #processamento de mensagem aqui

#                 sqs.delete_message(
#                     QueueUrl=fila_order_succeeded,
#                     ReceiptHandle=message['ReceiptHandle']
#                 )

# processar_mensagens_entrada()