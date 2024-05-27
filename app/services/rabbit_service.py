import os
import pika
import json
import pandas as pd
from typing import List
from bson import ObjectId

def json_serial(obj):
    if isinstance(obj, (pd.Timestamp, ObjectId)):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

def get_rabbitmq_connection():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=os.getenv('RABBITMQ_HOST','localhost'),
            port=int(os.getenv('RABBITMQ_PORT',5672)),
            credentials=pika.PlainCredentials(
                username=os.getenv('RABBITMQ_USER', 'guest'),
                password=os.getenv('RABBITMQ_PASSWORD', 'guest')
            )
        ))
        print("Connected to RabbitMQ")
        return connection
    except Exception as e:
        print(f"Failed to connect to RabbitMQ: {e}")
        raise

def batch_publish_to_queue(queue_name: str, messages: List[dict]):
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        
        for message in messages:
            channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=json.dumps(message, default=json_serial),
                properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
            )
        
        connection.close()
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Connection error: {e}")
    except pika.exceptions.ChannelError as e:
        print(f"Channel error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        