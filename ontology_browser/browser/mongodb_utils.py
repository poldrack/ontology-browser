from pymongo import MongoClient
from django.conf import settings
import datetime

def get_mongodb_connection():
    """Establish connection to MongoDB"""
    client = MongoClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_DB]
    return db

def get_task_collection():
    """Get the ontology-task collection"""
    db = get_mongodb_connection()
    return db['ontology-task']

def get_concept_collection():
    """Get the ontology-concept collection"""
    db = get_mongodb_connection()
    return db['ontology-concept']

def search_tasks(query, type_filter=None):
    """Search ontology-task collection"""
    collection = get_task_collection()
    
    search_conditions = []
    if query:
        search_conditions.append({
            '$or': [
                {'custom_id': {'$regex': query, '$options': 'i'}},
                {'description': {'$regex': query, '$options': 'i'}}
            ]
        })
    
    if type_filter and type_filter != 'all':
        search_conditions.append({'type': type_filter})
    
    final_query = {'$and': search_conditions} if search_conditions else {}
    return list(collection.find(final_query))

def search_concepts(query):
    """Search concepts collection by query in custom_id or description"""
    collection = get_concept_collection()
    
    if query:
        search_query = {
            '$or': [
                {'custom_id': {'$regex': query, '$options': 'i'}},
                {'description': {'$regex': query, '$options': 'i'}}
            ]
        }
    else:
        search_query = {}
    
    return list(collection.find(search_query))

def search_concepts_by_id(concept_id):
    """Search concepts collection by exact custom_id match"""
    collection = get_concept_collection()
    return list(collection.find({'custom_id': concept_id}))

def get_concept_by_id(concept_id):
    """Get a specific concept by its custom_id"""
    collection = get_concept_collection()
    return collection.find_one({'custom_id': concept_id})

def get_all_concepts():
    """Get all concepts from the collection"""
    collection = get_concept_collection()
    return list(collection.find())

def get_all_tasks():
    """Get all tasks from the collection"""
    collection = get_task_collection()
    return list(collection.find())

def get_task_by_id(task_id):
    """Get a specific task by its custom_id"""
    collection = get_task_collection()
    return collection.find_one({'custom_id': task_id})

def save_review(task_id, status, comment):
    """Save or update review for a task"""
    collection = get_task_collection()
    collection.update_one(
        {'custom_id': task_id},
        {
            '$set': {
                'review_status': status,
                'review_comment': comment,
                'review_date': datetime.datetime.now()
            }
        }
    )

def save_concept_review(concept_id, status, comment):
    """Save or update review for a concept"""
    collection = get_concept_collection()
    collection.update_one(
        {'custom_id': concept_id},
        {
            '$set': {
                'review_status': status,
                'review_comment': comment,
                'review_date': datetime.datetime.now()
            }
        }
    )

def load_jsonl_to_mongodb(jsonl_path, database_name, collection_name):
    """Coordinates the loading of JSONL data into MongoDB."""
    collection = get_mongodb_collection(database_name, collection_name)
    clear_collection(collection)  # Clear existing data
    documents = read_jsonl_file(jsonl_path)
    insert_documents(collection, documents)