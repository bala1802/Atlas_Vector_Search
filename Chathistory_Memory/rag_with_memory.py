import os
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import MessagesPlaceholder

from database_utils import get_db_connection
from database_utils import prepare_data
from database_utils import ingest_data
from database_utils import construct_vector_store
from database_utils import construct_retriever

from prompts import standalone_system_prompt, rag_system_prompt

# OpenAI Embeddings
embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"], model=os.environ["OPENAI_EMBEDDING_MODEL"])

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

# Prompt to Contextualize the User's current query based on the Chat-history
standalone_question_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", standalone_system_prompt), MessagesPlaceholder(variable_name="history"), ("human", "{question}"),
    ]
)

# Output Parser parses the result from LLM to String
parse_output = StrOutputParser()

# Runnable, which takes the Chat Message History and a follow-up question as input and creates a Standalone Question
question_chain = standalone_question_prompt | model | parse_output

# Retreiver Chain, accepts Context (Question Chain) obtained from the Retriever
retriever_chain = RunnablePassthrough.assign(context=question_chain | retriever | 
                                             (lambda docs: "\n\n".join([d.page_content for d in docs])))

# Prompt consisting of User's query, Retrieved Context and Chat History
rag_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", rag_system_prompt), MessagesPlaceholder(variable_name="history"), ("human", "{question}"),
    ]
)

# RAG chain - A runnable responsible for handling chat history messages for another runnable, including making updates
rag_chain = (retriever_chain | rag_prompt | model | parse_output)

# For the given Session-ID, the MongoDBChatMessageHistory instance is created, which holds the chat history retreived from the `history` collection.
def get_session_history(session_id: str) -> MongoDBChatMessageHistory:
    return MongoDBChatMessageHistory(os.environ["MONGO_DB_CONNECTION_STRING"], session_id, 
                                     database_name=os.environ["LANGCHAIN_CHATBOT_DB_NAME"], 
                                     collection_name=os.environ["HISTORY_CACHE_COLLECTION_NAME"])

# RAG chain with history
with_message_history = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

# User Queries Configured with the Session id
with_message_history.invoke({"question": "<User Query-1>"}, {"configurable": {"session_id": "1"}})

with_message_history.invoke({"question": "<Follow up Query, User Query-2>"}, {"configurable": {"session_id": "1"}})