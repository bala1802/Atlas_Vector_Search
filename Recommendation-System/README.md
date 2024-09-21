# Building a Recommendation System with MongoDB as a Vector Database and Hugging Face Embeddings

In this repository, I demonstrated how to build a simple recommendation system using MongoDB as a vector database and Hugging Face's models to generate vector embeddings. This system can be expanded by integrating it with a web interface, adding more sophisticated document preprocessing techniques, or experimenting with different similarity metrics and models.

MongoDB’s flexibility makes it a great starting point for storing and retrieving document vectors, while Hugging Face provides powerful pre-trained models that simplify the NLP tasks.

## Overview of the System

The recommendation system can be divided into two main phases:

- Document Embedding and Storage: The vector embeddings for each text document is generated using a pre-trained NLP model from Hugging Face. These vectors are then stored in MongoDB.
- Query Embedding and Search: When a user submits a query, a vector embedding for the query is generated using the same NLP model. This query vector is then used to search the MongoDB database for the most similar document vectors.

## Prerequisites

- `python` 3.10 or higher
- `MongoDB Atlas` instance
- Hugging Face `transformers` and `sentence-transformers` library for `embedding` generation
- `pymongo` library for interacting with MongoDB

### Packages Installation

`pip install pymongo transformers sentence-transformers`

## Process

### Step-1: Mongo DB Connection

Setting up a vector database connection using `pymongo`

![DB_Connection](https://github.com/user-attachments/assets/d8c5904f-2b7a-4333-8c06-b7055383855d)

### Step-2: Create Vector Index

The vector index is created in the MongoDB

<img width="476" alt="Screenshot 2024-09-21 at 9 46 28 AM" src="https://github.com/user-attachments/assets/8253c850-489e-4582-ae26-e78b9658abd8">


### Step-3: Vector Storage

Generate and store embeddings inside the Vector Database. The embeddings are generated through HuggingFace API

![EmbeddingsGeneration](https://github.com/user-attachments/assets/ee43c12b-a914-42b7-b189-1fd82e58b284)

### Step-4: Searching the Vector Database with a Query

When a user submits a query, the vectors are generated for the query and search the MongoDB database for the closest vectors.

![VectorSearch](https://github.com/user-attachments/assets/8252f727-c28f-45b6-b603-891724e41ebc)


### Step-5: Execution

![execution](https://github.com/user-attachments/assets/f46ec87b-e96d-48db-9686-c0a6eee3fa59)









