from pymongo import MongoClient
import json
from mongodb_utils import (
    load_jsonl_to_mongodb
)


def parse_jsonl_line(line):
    """Parses a single line of JSONL into a dictionary."""
    json_data = json.loads(line.strip())

    content = json_data['response']['body']['choices'][0]['message']['content']
    # clean up content
    content = content.replace("```json", "").replace("```", "")
    content_dict = json.loads(content)
    assert content_dict['type'] != 'other', f"type is other for {json_data['custom_id']}"
    content_dict['type'] = content_dict['type'].replace('construct-', '')
    content_dict['type'] = content_dict['type'].replace('_', ' ')
    content_dict['description'] = ''.join(content_dict['description'])
    content_dict['model'] = json_data['response']['body']['model']
    content_dict['custom_id'] = json_data['custom_id'].replace('task-','').replace('/','_')
    content_dict['system_fingerprint'] = json_data['response']['body']['system_fingerprint']
    return content_dict


if __name__ == "__main__":
    # Example usage
    jsonl_path = (
        "/Users/poldrack/Dropbox/data/ontology-learner/data/concept_results/"
        "batch_673d2908c74c81908932e5e6769a3c55.jsonl"
    )
    database_name = "ontology"
    collection_name = "ontology-concept"
    
    load_jsonl_to_mongodb(jsonl_path, database_name, collection_name, parse_jsonl_line)
