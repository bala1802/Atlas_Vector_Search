## Semantic Search Engine using OpenAI Embeddings MongoDB as Vector Database

In this article, I have walked through the process of creating a semantic search engine. This engine will generate vector embeddings for user queries and perform a semantic search by comparing those embeddings with documents stored in MongoDB. The vector embeddings are generated using OpenAI's `text-embedding-ada-002` model, and MongoDB is used to store and retrieve document vectors.

### What is Semantic Search?

Semantic search does the keyword matching by understanding the meaning and context of the query. In this repository, I've leveraged the vector embeddings (a numerical representations of text) to capture the semantic meaning and use these embeddings to find similar documents in the database.


### Packages

`pypi openai`
`pymongo`

### Prerequisites

- `OPENAI_API_KEY` for accessing the Embeddings model - `text-embedding-ada-002`
- `MongoDB Atlas` for the vector search

### Step-1: Setting up Mongo DB for Searching the Documents

![db_connection](https://github.com/user-attachments/assets/d8b18be0-8adb-4895-a24b-349bd2520f80)

### Step-2: Creating Atlas Vector index

<img width="429" alt="Vector Search Index" src="https://github.com/user-attachments/assets/4859c9f0-3e32-4d23-a5c2-ec6987dc5293">

### Step-3: Query Embedding and Semantic Search

For the given user query, the embedding for that particulat query is generated and then the search action is performed to find for the most similar document embeddings stored in MongoDB. 

![vector_search](https://github.com/user-attachments/assets/d426a890-8b02-45db-be94-d664e7d7431f)

### Step-4: Execution

![Execution](https://github.com/user-attachments/assets/175f16c4-ed53-46f7-b687-234a0f4a58e9)



