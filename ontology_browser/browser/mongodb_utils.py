from pymongo import MongoClient
from django.conf import settings

def get_mongodb_connection():
    """Establish connection to MongoDB"""
    client = MongoClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_DB]
    return db

def get_ontology_collection():
    """Get the ontology-task collection"""
    db = get_mongodb_connection()
    return db['ontology-task'] 

def search_ontology(query, type_filter=None):
    """Search ontology-task collection by custom_id or description with optional type filter"""
    collection = get_ontology_collection()
    
    # Create base query for text search
    search_conditions = []
    if query:
        search_conditions.append({
            '$or': [
                {'custom_id': {'$regex': query, '$options': 'i'}},
                {'description': {'$regex': query, '$options': 'i'}}
            ]
        })
    
    # Add type filter if specified
    if type_filter and type_filter != 'all':
        search_conditions.append({'type': type_filter})
    
    # Combine conditions
    final_query = {'$and': search_conditions} if search_conditions else {}
    
    return list(collection.find(final_query))

def get_all_tasks():
    """Get all tasks from the collection"""
    collection = get_ontology_collection()
    return list(collection.find())

def get_task_by_id(task_id):
    """Get a specific task by its custom_id"""
    collection = get_ontology_collection()
    return collection.find_one({'custom_id': task_id})