## Adding Memory to the RAG application using MongoDB and LangChain

Conversations between the Large Language Model (LLM) and the user are saved and retrieved to maintain a coherent, context-aware interaction history. This historical reference offers additional context, allowing the LLM to better understand previous interactions, which helps the chatbot generate more accurate and relevant responses to user queries.

### Libraries

- `pypi datasets`: to access a variety of datasets available on the HuggingFace Hub.
- `pypi langchain`: toolkit designed for working with the LangChain framework, which allows the chaining of LLMs for different tasks.
- `pypi langchain-mongodb`: to integrate MongoDB with LangChain, enabling it to be used as a vector store, semantic cache, and to store chat history.
- `pypi langchain-openai`: to integrate OpenAI models within the LangChain framework.
- `pypi pymongo`: Interactiong with MongoDB database

### Database Set-up

#### `database_utils.get_db_connection`: To establish a MongoDB connection for the provided Connection uri
![db_connection](https://github.com/user-attachments/assets/627b462c-0248-4250-b6f3-726a28402bf8)

#### Create Collections: `data` and `history`.

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

#### Data Preparation `database_utils.prepare_data`

![data_preparation](https://github.com/user-attachments/assets/f444486b-beec-4693-9889-9c86aba23934)



