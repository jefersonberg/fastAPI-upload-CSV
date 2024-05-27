from typing import List, Union
from pymongo import MongoClient
from bson import ObjectId
from app.db.mongodb import get_database

def serialize_doc(doc):
    """Converts ObjectId to string in a MongoDB document."""
    if '_id' in doc and isinstance(doc['_id'], ObjectId):
        doc['_id'] = str(doc['_id'])
    return doc

def find_debt_by_field(field_name: str, field_value: Union[str, int]):
    db = get_database()
    collection = db["debts"]
    query = {field_name: field_value}
    results = collection.find(query)
    return [serialize_doc(doc) for doc in results]

def find_debt(governmentId: str = None, email: str = None, debtId: str = None) -> List[dict]:
    if governmentId:
        return find_debt_by_field("governmentId", governmentId)
    elif email:
        return find_debt_by_field("email", email)
    elif debtId:
        return find_debt_by_field("debtId", debtId)
    else:
        return []
