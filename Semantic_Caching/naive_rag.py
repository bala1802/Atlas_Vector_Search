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

embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"], 
                              model=os.environ["OPENAI_EMBEDDING_MODEL"])

client = get_db_connection(mongodb_connection_uri=os.environ["MONGO_DB_CONNECTION_STRING"])

data = prepare_data()
ingest_data(client=client, collection_name=os.environ["DATA_COLLECTION_NAME"], 
            db_name=os.environ["LANGCHAIN_CHATBOT_DB_NAME"], data=data)

vector_store = construct_vector_store(embeddings=embeddings,
                                      db_name=os.environ["LANGCHAIN_CHATBOT_DB_NAME"],
                                      collection_name=os.environ["DATA_COLLECTION_NAME"],
                                      mongodb_connection_uri=os.environ["MONGO_DB_CONNECTION_STRING"],
                                      atlas_vector_search_index_name=os.environ["ATLAS_VECTOR_SEARCH_INDEX_NAME"],
                                      )
retriever = construct_retriever(vector_store=vector_store)

retrieve = {"context": retriever | (lambda docs: "\n\n".join([d.page_content for d in docs])), "question": RunnablePassthrough()}
template = """Answer the question based only on the following context: \
{context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI(temperature=0, openai_api_key=os.environ["OPENAI_API_KEY"])

parse_output = StrOutputParser()

naive_rag_chain = (retrieve | prompt | model | parse_output)
naive_rag_chain.invoke("What is the best movie to watch?")

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

naive_rag_chain.invoke("What is the best movie to watch?")