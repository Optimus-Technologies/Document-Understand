import streamlit as st
from functions import chat_with_data, extract_all_data, summarize_documents
import uuid
# from document_model import model, parser

# Set up page configuration
st.set_page_config(layout="wide")

# Initialize session state for messages if not already done
if 'all_messages' not in st.session_state:
    st.session_state.all_messages = []

if 'category' not in st.session_state:
    st.session_state['category']= ''

if 'followups' not in st.session_state:
    st.session_state['followups'] = []

# Display the subheader if there are no messages
if len(st.session_state.all_messages) == 0:
    st.markdown("<h2 style='text-align: center;'>How can I help?</h2>", unsafe_allow_html=True)
 

def reset_to_new_chat():
    
    st.session_state.all_messages = []
    st.session_state['category']= ''
    st.session_state['followups'] = []




# Sidebar setup
st.sidebar.title('UDOCX 🤖')
colmn1, colmn2, = st.sidebar.columns(2)
button = colmn1.button("New Chat")
if button:
    reset_to_new_chat()
    uploaded_files = []
    st.rerun()
st.sidebar.divider()

# Dialog function
@st.dialog("Upgrade to premium")
def dialogue():
    st.write("Upgrade to pro and you can upload larger sizes of data")
    st.write("Premium users can perform unlimited quick searches, allowing for fast access to information.")
    if st.button("Upgrade"):
        st.session_state.upgrade = {"upgrade": "true"}
        st.rerun()


option = st.sidebar.selectbox(
    "What type of documents Are we dealing with ?",
    ("General","Agriculture", "Land Administration", "Healthcare", "Finance And Banking", "Education", "Receipts"),
)

if option:
    st.session_state['category'] = option

st.sidebar.write(f"📍 {st.session_state.category}")



uploaded_files = st.sidebar.file_uploader("Choose files 🗃️", accept_multiple_files=True)

col1, col2 = st.sidebar.columns(2)
if col1.button("Extract key Info ⚡"):
    text = extract_all_data(uploaded_files, category=st.session_state.category)
    st.write(text)

if col2.button("Summarize Documents"):
    text = summarize_documents(uploaded_files, category=st.session_state.category)
    st.write(text)


if uploaded_files:
    st.sidebar.subheader("Uploaded Files:")

    for uploaded_file in uploaded_files:
        st.sidebar.write(f"**File Name:** {uploaded_file.name}")

   



if not uploaded_files:
    st.markdown("<h2 style='text-align: center;'>Upload documents for extraction  📄 </h2>", unsafe_allow_html=True)

# Chat input and message handling

prompt = st.chat_input("Your message", key='prompt')

if prompt:
    st.session_state.all_messages.append({'user': 'user', 'message': prompt})
    text = chat_with_data(uploaded_files, st.session_state.all_messages, prompt, category=st.session_state['category'])

    response_ai = text.get('answer')
    follow_ups = text.get('followups')
    st.session_state['followups'] = follow_ups
    st.session_state.all_messages.append({'user': '🤖', 'message': response_ai})



def fetech_data():
    return st.session_state.all_messages


# Display all messages
if len(st.session_state.all_messages) > 0:
    for message in st.session_state.all_messages:
        match message.get('user'):
            case 'user':
                st.html(f"<h2>{message.get('message')}</h2>")
            case _:
                msg = message.get('message')
                print(msg)
                # st.write_stream(stream_data(msg))
                st.write(f"{message.get('user')}: {message.get('message')}")
    
#Display follow_ups
# Replace the existing followup display code with this:
if st.session_state['followups']:
    st.subheader("Suggested followup questions:")
    for followup in st.session_state['followups']:
        if st.button(followup):
            text = chat_with_data(uploaded_files, st.session_state.all_messages, followup, category=st.session_state['category'])
            response_ai = text.get('answer')
            new_followups = text.get('followups')
            st.session_state['followups'] = new_followups
            st.session_state.all_messages.append({'user': 'user', 'message': followup})
            st.session_state.all_messages.append({'user': '🤖', 'message': response_ai})
            st.rerun()


# st.write(followup + "\n" for followup in st.session_state.followups)


# Sidebar options and file uploader
st.sidebar.subheader("Chatbot Options")
if st.sidebar.button("Become a Pro 💵 "):
    dialogue()
# Additional sidebar section

st.sidebar.subheader("Optimus")
st.sidebar.subheader(" made with 🇬 🇭  🇬🇭 🇬🇭 ") 
