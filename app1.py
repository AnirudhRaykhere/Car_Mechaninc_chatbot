import streamlit as st
from streamlit_chat import message
from utils2 import get_response

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# UI
st.set_page_config(page_title='Chatbot', page_icon='🚗')
st.markdown("<h1 style='text-align:center;'>How can I assist you today?</h1>", unsafe_allow_html=True)
response_container = st.container()
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_input("You: ", key="user_input")
        # user_input = st.text_area("Your question goes here:", key='input', height=5)
        submit_button = st.form_submit_button(label='Send')
        
        if submit_button and user_input:
            # Append user input to messages
            st.session_state['messages'].append(user_input)
            
            # Get model response
            model_response = get_response(user_input)
            
            # Append model response to messages
            st.session_state['messages'].append(model_response)
            
            # Display conversation
            with response_container:
                for i in range(len(st.session_state['messages'])):
                    if (i % 2) == 0:
                        message(st.session_state['messages'][i], is_user=True, key=str(i) + '_user')
                    else:
                        message(st.session_state['messages'][i], key=str(i) + '_AI')
