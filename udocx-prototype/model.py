from google.generativeai import GenerativeModel, configure
import ast
from api_keys import client

#Using Groq
# Initialize the Groq client



# Initialize the Gemini client
# model = GenerativeModel('gemini-1.5-pro')

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

def extract_info(text: str, category: str, query: str, chat_history: str):
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
                        Do not consider an in the documents provided to you that do
                        not relate to the question asked.

                    Below is your chat history:
                    {chat_history}
                    
                    The documents from which you will extract is provided below:
                    {text}

                    Below is the question the user wants you to answer:
                    '''

    chat_completion = client.chat.completions.create(
        messages=[{"role": "system", 
                   "content": full_prompt}, 
                   {
            "role": "user",
            "content": query,
            }
        ],
        model="llama-3.1-8b-instant",
    )
    
    
    key_info = chat_completion.choices[0].message.content
    # response = model.generate_content(full_prompt)
    
    # Get the raw text response
    return key_info


def suggest_followups(text: str, chat_history: str):
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

                    NOTE:
                    Pay much more attention to the chat_history when giving a response
                    Follow strictly the output format specified.
                    Do NOT output anything else before or after the specified response format
                '''
    
    

    chat_completion = client.chat.completions.create(
        messages=[{"role": "system", 
                   "content": full_prompt}, 
                   {
            "role": "user",
            "content": "Suggest three followups",
            }
        ],
        model="llama-3.1-8b-instant",
    )
    
    
    follow_ups = chat_completion.choices[0].message.content
    # response = model.generate_content(full_prompt)
    followup_list = ast.literal_eval(follow_ups)
    # Get the raw text response
    return followup_list


def extract_all_key_info(text: str, category: str):
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
                    document by document.
                            

                    Below are the documents:\
                    {text}
                    
                    Take into consideration this furthur directives before giving an output\
                    
                    Below is the further directives:\
                    {prompt}

                    Your output should be in this format.\
                    A markdown with the name of the file a title
                    Example:
                    File1.pdf
                    Name:
                    Andrew James
                    Email:
                    andrewjames@gmail.com
                '''
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "system", 
                   "content": full_prompt}, 
                   {
            "role": "user",
            "content": "Extract all key information from the documents",
            }
        ],
        model="llama-3.1-8b-instant",
    )
    
    
    key_info = chat_completion.choices[0].message.content
    # response = model.generate_content(full_prompt)
    
    # Get the raw text response
    return key_info



def summarizer(text: str, category: str):
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
                    Summarize the documents one at a time\
                    document by document.
                            

                    Below are the documents:\
                    {text}
                    
                    Take into consideration this furthur directives before giving an output\
                    
                    Below is the further directives:\
                    {prompt}

                    Your output should be in this format.\
                    A markdown with the name of the file a title
                    Example:
                    File1.pdf
                    Summary from File1.pdf
                    File2.pdf
                    Summary from File2.pdf
                '''
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "system", 
                   "content": full_prompt}, 
                   {
            "role": "user",
            "content": "Summmarize the documents",
            }
        ],
        model="llama-3.1-8b-instant",
    )
    
    
    summary = chat_completion.choices[0].message.content
    # response = model.generate_content(full_prompt)
    
    # Get the raw text response
    return summary
