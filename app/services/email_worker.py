import os
import pika
import json
from app.services.email_service import send_email
from app.db.mongodb import get_database
from bson import ObjectId

def callback(ch, method, properties, body):
    message = json.loads(body)
    try:
        send_email(message['email'], "Debt Notification", f"Your debt is due on {message['debtDueDate']}.")
        update_debt_status(message['_id'])
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Failed to send email: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

def update_debt_status(debt_id):
    db = get_database()
    collection = db["debts"]
    collection.update_one({"_id": ObjectId(debt_id)}, {"$set": {"emailSent": True}})

def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST'),
        port=int(os.getenv('RABBITMQ_PORT'))
    ))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='email_queue', on_message_callback=callback)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    start_worker()
