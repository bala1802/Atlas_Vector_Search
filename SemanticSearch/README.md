## Semantic Search Engine using OpenAI Embeddings MongoDB as Vector Database

In this article, I have walked through the process of creating a semantic search engine. This search engine will generate vector embeddings for user queries and perform a semantic search by comparing those embeddings with documents stored in MongoDB. The vector embeddings are generated using OpenAI's text-embedding-ada-002 model, and MongoDB is used to store and retrieve document vectors.

### What is Semantic Search?

Semantic search does the keyword matching by understanding the meaning and context of the query. In this repository, I've leveraged the vector embeddings (a numerical representations of text) to capture the semantic meaning and use these embeddings to find similar documents.


### Packages

`pypi openai`
`pymongo`

### Prerequisites

- `OPENAI_API_KEY` for accessing the Embeddings model - `text-embedding-ada-002`
- `MongoDB Atlas` for the vector search
