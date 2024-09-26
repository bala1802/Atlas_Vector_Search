

from datasets import load_dataset
from pymongo import MongoClient
import pandas as pd

from langchain_openai import OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch

from dotenv import load_dotenv
load_dotenv()

'''
Author: Balaguru Sivasambagupta
Github: https://github.com/bala1802
'''
def prepare_data():
    data = load_dataset("MongoDB/embedded_movies")
    df = pd.DataFrame(data["train"])
    df = df[df["fullplot"].notna()]
    df.rename(columns={"plot_embedding": "embedding"}, inplace=True)
    return df

'''
Author: Balaguru Sivasambagupta
Github: https://github.com/bala1802
'''
def ingest_data(client, db_name, collection_name, data):
    collection = client[db_name][collection_name]
    collection.delete_many({})
    records = data.to_dict('records')
    collection.insert_many(records)

'''
Author: Balaguru Sivasambagupta
Github: https://github.com/bala1802
'''
def get_db_connection(mongodb_connection_uri):
    client = MongoClient(mongodb_connection_uri)
    try:
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
    return None

'''
Author: Balaguru Sivasambagupta
Github: https://github.com/bala1802
'''
def construct_vector_store(mongodb_connection_uri, db_name, 
                           embeddings, collection_name, 
                           atlas_vector_search_index_name):
    vector_store = MongoDBAtlasVectorSearch.from_connection_string(
        connection_string = mongodb_connection_uri,
        namespace = db_name + "." + collection_name,
        embedding = embeddings,
        index_name = atlas_vector_search_index_name,
        text_key="fullplot"
    )
    return vector_store

'''
Author: Balaguru Sivasambagupta
Github: https://github.com/bala1802
'''
def construct_retriever(vector_store):
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    return retriever