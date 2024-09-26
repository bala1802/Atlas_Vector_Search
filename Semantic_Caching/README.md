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
