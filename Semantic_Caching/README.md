## Enabling Semantic Caching to the RAG application using LangChain and MongoDB

Integrating Semantic Caching into a Retrieval Augmented Generated application can be seamlessly achieved using the LangChain-MongoDB framework. In this repository I have outlined the steps involved in ena=hancing the RAG architecture with Semantic Caching, which optimizes performance and lowers operational costs. By caching both user queries and their corresponding responses, 
the application can efficiently retrieve stored results for semantically similar future queries. This approach minimizes redundant API calls to the large language model (LLM) provider, leading to reduced latency and significantly lowering the cost of maintaining the RAG system.

### Semantic Caching Architecture

![architecture](https://github.com/user-attachments/assets/0a38b33d-c185-4f29-8bfe-c8055c613e28)
Source: MongoDB

### Libraries

- `pypi datasets`: to access a variety of datasets available on the HuggingFace Hub.
- `pypi langchain`: toolkit designed for working with the LangChain framework, which allows the chaining of LLMs for different tasks.
- `pypi langchain-mongodb`: to integrate MongoDB with LangChain, enabling it to be used as a vector store, semantic cache, and to store chat history.
- `pypi langchain-openai`: to integrate OpenAI models within the LangChain framework.
- `pypi pymongo`: Interactiong with MongoDB database

### Database Set-up

#### `database_utils.get_db_connection`: To establish a MongoDB connection for the provided Connection uri
![db_connection](https://github.com/user-attachments/assets/627b462c-0248-4250-b6f3-726a28402bf8)

#### Create Collections: `data` and `semantic_cache`.

#### Create Search Vector Index for `data` collection. ATLAS VECTOR SEARCH INDEX NAME: `vector_index`

```
{
  "fields": [
    {
      "numDimensions": 1536,
      "path": "embedding",
      "similarity": "cosine",
      "type": "vector"
    }
  ]
}
```

#### Create Vector Index for `semantic_cache` collection. ATLAS VECTOR SEARCH INDEX NAME: `vector_index`

```
{
  "fields": [
    {
      "numDimensions": 1536,
      "path": "embedding",
      "similarity": "cosine",
      "type": "vector"
    },
    {
      "path": "llm_string",
      "type": "filter"
    }
  ]
}
```

#### Data Preparation `database_utils.prepare_data`

![data_preparation](https://github.com/user-attachments/assets/f444486b-beec-4693-9889-9c86aba23934)

#### Data Ingestion `database_utils.ingest_data`

![data_ingestion](https://github.com/user-attachments/assets/c0ab72da-a6f9-4104-bcbf-80a8a89a3270)

#### Vector Store Construction for Storing the embeddings of the documents

![vector_store](https://github.com/user-attachments/assets/d52c597a-e864-4fb3-a644-9b016452c9c3)

#### Retriever Object to extract the similar documents for the given User Query

![vector_store](https://github.com/user-attachments/assets/299702bf-c767-4016-87cf-e0813231766e)

### Semantic Cache Layer

![semantic_cache_layer](https://github.com/user-attachments/assets/d049305d-b914-4701-9d52-c8701ac6902c)

- `MongoDBAtlasSemanticCache` acts as an interface for connecting to MongoDB and setting up a semantic cache store.
- Provides API methods to:
  
      - Initialize the cache.
      - Retrieve cached responses based on user query prompts and LLM outputs.
      - Update the cache with new responses.
      - Clear cached entries entirely or based on specific criteria.

#### Execution

![semantic_cache_execution](https://github.com/user-attachments/assets/27ed6515-4c28-4296-941e-7b9d38d1a0a0)
