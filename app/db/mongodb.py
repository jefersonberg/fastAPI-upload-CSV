from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.MONGO_URI)
database = client["kanastra"]

def get_database():
    return database

def init_db():
    if "debts" not in database.list_collection_names():
        database.create_collection("debts")