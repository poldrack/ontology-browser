from pymongo import MongoClient
import json


def get_mongodb_collection(database_name, collection_name, connection_url='mongodb://localhost:27017/'):
    """Establishes connection and returns MongoDB collection."""
    client = MongoClient(connection_url)
    db = client[database_name]
    # create collection if it doesn't exist
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
    return db[collection_name]



def read_jsonl_file(jsonl_path):
    """Reads and parses JSONL file, yielding documents."""
    with open(jsonl_path, 'r') as file:
        for line in file:
            try:
                parsed_entry = parse_jsonl_line(line)
                yield parsed_entry
            except Exception as e:
                print(f"Error parsing line {line}: {e}")
                continue


def insert_documents(collection, documents):
    """Inserts documents into MongoDB collection if they don't already exist."""
    inserted_count = 0
    skipped_count = 0
    
    for document in documents:
        # Check if document already exists using custom_id
        if not collection.find_one({'custom_id': document['custom_id']}):
            collection.insert_one(document)
            inserted_count += 1
        else:
            skipped_count += 1
    
    print(f"Processed documents for {collection.full_name}:")
    print(f"- Inserted: {inserted_count}")
    print(f"- Skipped (already exists): {skipped_count}")


def clear_collection(collection):
    """Removes all documents from the specified collection."""
    result = collection.delete_many({})
    print(f"Cleared {result.deleted_count} documents from {collection.full_name}")


def load_jsonl_to_mongodb(jsonl_path, database_name, collection_name):
    """Coordinates the loading of JSONL data into MongoDB."""
    collection = get_mongodb_collection(database_name, collection_name)
    clear_collection(collection)  # Clear existing data
    documents = read_jsonl_file(jsonl_path)
    insert_documents(collection, documents)