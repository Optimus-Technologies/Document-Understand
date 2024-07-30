from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, AnyMessage
import os
from typing import List

#Hugging Face with langchian
os.environ["HUGGINGFACE_API_TOKEN"] = "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"

model = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.3")

chatmodel = ChatHuggingFace(llm=model)

async def chat_with_model(query: str, document: str, chat_history: List[AnyMessage] = []):
    messages = [SystemMessage(content=document)]
    messages += chat_history
    human_message = HumanMessage(content=query)
    messages.append(human_message)

    response = chatmodel.invoke(messages)

    messages.append(AIMessage(content=response.content))
    return response
 

from groq import Groq

#Using Groq
# Initialize the Groq client
client = Groq(api_key="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")

# Function to extract key information using Groq AI
async def extract_key_info(text):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'system',
                'content': 'Act as a well-trained NER model. You are to extract the key features of the text I provide you. Do a very great job and return the information in a structured format.in a situation where a user upload a general file which is not anything related to NER, then summarize the key points'
            },
            {
                "role": "user",
                "content": text,
            }
        ],
        model="llama3-8b-8192",
    )
    
    # Get the raw text response
    key_info = chat_completion.choices[0].message.content
    return key_info


#Function to answer questions based on document
async def question_answer(query: str, document: str, chat_history: List[str]):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'system',
                'content': f'''Act as a well-trained question and answer model.\
                You are to answer questions only from the text I provide you below.\
                Do a very great job and return your answer in a structured format.\
                In a situation where you cannot find an answer to the question based\
                on the text, do not forge an answer.
                
                ```text```
                {document}
                '''
            },
        ] + chat_history + [{
                "role": "user",
                "content": query,
            }],
        model="llama3-8b-8192",
    )
    
    # Get the raw text response
    response = chat_completion.choices[0].message.content
    return response