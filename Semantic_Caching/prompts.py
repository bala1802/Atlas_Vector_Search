'''
Author: Balaguru Sivasambagupta
Github: https://github.com/bala1802
'''

standalone_system_prompt = """
Given a chat history and a follow-up question, rephrase the follow-up question to be a standalone question. 
Do NOT answer the question, just reformulate it if needed, otherwise return it as is. 
Only return the final standalone question.
"""

rag_system_prompt = """Answer the question based only on the following context: 
{context}
"""