'''
Author: Balaguru Sivasambagupta
Github: https://github.com/bala1802
'''

import os
import requests
from dotenv import load_dotenv

from openai import OpenAI
from pymongo.mongo_client import MongoClient

load_dotenv()

openai_client = OpenAI()

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
    text = text.replace("\n", "")
    return openai_client.embeddings.create(input=[text], model=os.environ["OPENAI_EMBEDDING_MODEL"]).data[0].embedding

def vector_search(user_query, collection):
    results = collection.aggregate(
                                    [
                                        {
                                            "$vectorSearch": 
                                            {
                                                "queryVector": generate_embeddings(text=user_query),
                                                "path": "plot_embedding",
                                                "numCandidates": 100,
                                                "limit": 4,
                                                "index": "PlotSemanticSearch",
                                            }
                                        }
                                    ]
                                )
    return results

if __name__ == "__main__":
    mongodb_client = get_db_connection(uri=os.environ["MONGO_DB_CONNECTION_STRING"])
    db = mongodb_client.sample_mflix
    collection = db.embedded_movies

    results = vector_search(user_query="Scientific movies involving crime and action sequences", collection=collection)
    
    for document in results:
        print(f'Movie Name: {document["title"]}, \nMovie Plot: {document["plot"]}\n')