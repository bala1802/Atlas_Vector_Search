'''
Author: Balaguru Sivasambagupta
Github: https://github.com/bala1802
'''

import os
import requests
from dotenv import load_dotenv

from pymongo.mongo_client import MongoClient

load_dotenv()

embedding_url = os.environ["EMBEDDING_URL"]
hf_token = os.environ["HUGGING_FACE_TOKEN"]

def get_db_connection(uri):
    client = MongoClient(uri)
    try:
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
    return None

def generate_embeddings(text: str) -> list[float]:
    response = requests.post(embedding_url,
                             headers={"Authorization": f"Bearer {hf_token}"},
                             json={"inputs": text})
    
    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")

    return response.json()

def create_embeddings(collection):
    for doc in collection.find({'plot':{"$exists": True}}).limit(50):
        doc['plot_embedding_hf'] = generate_embeddings(doc['plot'])
        collection.replace_one({'_id': doc['_id']}, doc)

def vector_search(user_query, collection):
    results = collection.aggregate(
                                    [
                                        {
                                            "$vectorSearch":
                                            {
                                                "queryVector": generate_embeddings(user_query),
                                                "path": "plot_embedding_hf",
                                                "numCandidates": 50,
                                                "limit": 4,
                                                "index": "vector_index"
                                            }
                                        }
                                    ]
                                )
    
    return results

if __name__ == "__main__":
    client = get_db_connection(uri=os.environ["MONGO_DB_CONNECTION_STRING"])
    db = client.sample_mflix
    collection = db.movies

    for doc in collection.find({'plot':{"$exists": True}}):
        doc['plot_embedding_hf'] = generate_embeddings(doc['plot'])
        collection.replace_one({'_id': doc['_id']}, doc)
    
    results = vector_search(user_query="Scientific movies involving crime and action sequences")
    for document in results:
        print(f'Movie Name: {document["title"]}, \nMovie Plot: {document["plot"]}\n')
