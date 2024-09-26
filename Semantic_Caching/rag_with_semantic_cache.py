'''
Author: Balaguru Sivasambagupta
Github: https://github.com/bala1802
'''

import os

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.globals import set_llm_cache
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_mongodb.cache import MongoDBAtlasSemanticCache

from database_utils import get_db_connection
from database_utils import prepare_data
from database_utils import ingest_data
from database_utils import construct_vector_store
from database_utils import construct_retriever

# OpenAI Embeddings
embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"], model=os.environ["OPENAI_EMBEDDING_MODEL"])

# Enabing the Semantic Cache Layer
set_llm_cache(
    MongoDBAtlasSemanticCache(
        connection_string=os.environ["MONGO_DB_CONNECTION_STRING"],
        embedding=embeddings,
        collection_name=os.environ["SEMANTIC_CACHE_COLLECTION_NAME"],
        database_name=os.environ["LANGCHAIN_CHATBOT_DB_NAME"],
        index_name=os.environ["ATLAS_VECTOR_SEARCH_INDEX_NAME"],
        wait_until_ready=True
    )
)

# OpenAI Model
model = ChatOpenAI(temperature=0, openai_api_key=os.environ["OPENAI_API_KEY"])

# Database Connection
client = get_db_connection(mongodb_connection_uri=os.environ["MONGO_DB_CONNECTION_STRING"])

# Prepare Data
data = prepare_data()

# Ingest Data to the Mongo DB for the specified Collection
ingest_data(client=client, collection_name=os.environ["DATA_COLLECTION_NAME"], db_name=os.environ["LANGCHAIN_CHATBOT_DB_NAME"], data=data)

# Vector Store Construction for storing the embeddings of the documents
vector_store = construct_vector_store(embeddings=embeddings, db_name=os.environ["LANGCHAIN_CHATBOT_DB_NAME"],
                                      collection_name=os.environ["DATA_COLLECTION_NAME"],
                                      mongodb_connection_uri=os.environ["MONGO_DB_CONNECTION_STRING"],
                                      atlas_vector_search_index_name=os.environ["ATLAS_VECTOR_SEARCH_INDEX_NAME"],
                                      )

# Retriever Object to extract the similar documents for the given User Query
retriever = construct_retriever(vector_store=vector_store)

retrieve = {"context": retriever | (lambda docs: "\n\n".join([d.page_content for d in docs])), "question": RunnablePassthrough()}
template = """Answer the question based only on the following context: \
{context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

# Output Parser parses the result from LLM to String
parse_output = StrOutputParser()

# RAG chain - A runnable responsible for handling chat history messages for another runnable, including making updates
naive_rag_chain = (retrieve | prompt | model | parse_output)

naive_rag_chain.invoke("What is the best movie to watch?") # Initial Call

naive_rag_chain.invoke("What is the best movie to watch?") # Retrieves response from the semantic cache