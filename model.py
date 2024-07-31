import os
from typing import List
from langchain_core.documents import Document
from google.generativeai import GenerativeModel, configure



# Initialize the Gemini client
configure(api_key='AIzaSyAs9e2qHGqLrEg-E6hxGNueIwPwX6lq9Fk')
model = GenerativeModel('gemini-1.5-pro')

prompts = {
        "Healthcare": '''
            You are a professional medical doctor. You are very good at extracting key information
            from healthcare related data such as extracting patient information, medical history, 
            and treatment plans from hospital records, insurance claims, and medical research papers without any errors.
        ''',
        "Agriculture": '''
            You are a professional agricultural engineer. You are very good at extracting key information
            from agriculture related data such as farm records, crop insurance documents, and market reports
            to support decision- making for farmers, agricultural businesses, and policymakers.
        ''',
        "Finance and Banking": '''
            You are a professional finance and banking practioner. You are very good at extracting financial information
            from finance and banking related data such as bank statements, loan applications, and investment documents
            to support credit scoring, risk assessment, and financial inclusion.
        ''',
        "Education": '''
            You work as a  data analyst at an educational institute. You are very good at extracting key information
            from education related data such as extractstudentinformation,academic records, and learning outcomes
            from school databases, exam papers, and research articles to support education policy and improvement.
        ''',
        "Land Administration": '''
            You work as a land economist. You are very good at extracting useful information from data related to land
            administration for extract property information, ownership details, and transaction history from land deeds,
            property titles, and court documents to support land reform, property rights, and urban planning.
        ''',
        "Receipt": '''
            You are a very good at retrieving key information such as vendor information,
            purchase details, payment information from receipts and invoices. 
        '''
    }

async def extract_info(text: str, category: str, query: str, chat_history: str):
    # Define prompts for each category
    

    # Choose the appropriate prompt based on the category
    if category in prompts:
        prompt = prompts[category]
    else:
        prompt = "You are a very good question and answer system\n"

    # Construct the full prompt
    full_prompt = f'''Act as a well-trained NER model.\
                    You are to provide the info for all that the\
                    user need. Dont start with introducing yourself,\
                    go straight to the point. i will tip you\
                    $500 when you do a really exceptional job.

                    
                    Take into consideration your chat history which will be provided\
                    to you before the user asks his question.

                    Consider also this directive before giving an answer {prompt}

                    REMEMBER:
                        Be precise and concise

                    Below is your chat history:
                    {chat_history}
                    
                    The documents from which you will extract is provided below:
                    {text}

                    Below is the question the user wants you to answer:
                    {query}
                    '''


    response = model.generate_content(full_prompt)
    
    # Get the raw text response
    return response.text


async def suggest_followups(text: str, chat_history: str):
    full_prompt = f'''Act as a well-trained NER model.\
                    You are to provide the info for all that the\
                    user need. Dont start with introducing yourself,\
                    go straight to the point. i will tip you\
                    $500 when you do a really exceptional job.

                    The user will provide you with one or more documents\
                    based on the documents suggest 3 likely followup questions\
                    the user may ask.\
                            

                    Below are the documents:\
                    {text}
                    
                    Take also into consideration the chat history of the user\
                    
                    Below is the chat history:\
                    {chat_history}

                    Your output should be in this format.\
                    Example:\
                    ["What is the name of the person?", "How old is Martins?", "What is the total cost in the invoice?"]
                '''
    
    

    response = model.generate_content(full_prompt)
    return response.text



async def extract_all_key_info(text: str, category: str):
    if category in prompts:
        prompt = prompts[category]
    else:
        prompt = "You are a very good question and answer system\n"

    full_prompt = f'''Act as a well-trained NER model.\
                    You are to provide the info for all that the\
                    user need. Dont start with introducing yourself,\
                    go straight to the point. i will tip you\
                    $500 when you do a really exceptional job.

                    The user will provide you with one or more documents\
                    Extract all the key information from the documents\
                    document by document
                            

                    Below are the documents:\
                    {text}
                    
                    Take into consideration this furthur directives before giving an output\
                    
                    Below is the further directives:\
                    {prompt}

                    Your output should be in this format.\
                    [{"file1.pdf": "Key info extracted from file1.pdf"},\
                    {"file2.pdf": "Key info extracted from file2.pdf"}]
                '''
    

    response = model.generate_content(full_prompt)
    return response.text
