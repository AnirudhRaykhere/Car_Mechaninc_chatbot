from langchain_community.llms import Cohere
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import os
import warnings
import streamlit as st
from streamlit_chat import message
warnings.filterwarnings("ignore")
os.environ['COHERE_API_KEY']='d7TP509U4vjmFcXmxQD0YFizCOeXBaZzq3K77SFs'

if 'conversation' not in st.session_state:
    st.session_state['conversation'] =None
if 'messages' not in st.session_state:
    st.session_state['messages'] =[]


def get_response(user_input):
    if st.session_state['conversation'] is None:
        llm=Cohere(temperature=0.7)

        # prompt1=PromptTemplate(
        #     input_variables=["question"],
        #     template="""
        #     Task: You are a vehicle problem solving chatbot which respond politely with users.
        #     Instructions: 1. If user have any problem related to one's vehicle then you have to ask them model name, model year and the specific problem
        #                 2. if user give all the details then this is the final output
        #                 3. if user do not give all the details then you keep asking them model name, model year and the specific problem.
        #     user quesion: {question}    """
        # )

        # memory=ConversationBufferMemory(input_key='question',memory_key='chat_history')

        # chain1=LLMChain(
        #     llm=llm,
        #     prompt=prompt1,
        #     memory=memory,
        #     output_key='response',
        #     verbose=True
        # )

        # # print(chain1.run('Hello'))

        # prompt2=PromptTemplate(
        #     input_variables=["response"],
        #     template=""" 
        #     Task: from previous response you have to give the solution for the problem of vehicle
        #     Instructions: 1. you have model name, model year and the specific problem of the vehicle.
        #                 2. Keeping all these details, you have to solve the vehicle problem.
        #     previous_response={response}    """
        # )

        # chain2=LLMChain(
        #     llm=llm,
        #     prompt=prompt2,
        #     memory=memory,
        #     output_key='final_response',
        #     verbose=True
        # )

        # st.session_state['conversation']=SequentialChain(
        #     chains=[chain1, chain2],
        #     input_variables=['question'],
        #     # output_variable=['final_response'],
        #     memory=memory,
        #     verbose=True
        # )
        
        prompt=PromptTemplate(
            input_variables=["input","history"],
            template="""
            Task: you are a vehicle repairing solution providing chatbot.
            Instructions: 1. If user have any problem related to one's vehicle then you have to ask them model name, model year and the specific problem.
                   2. if user provide model name, car maufacturing year, problem in the car then only  provide them solution.
                   3. if user do not give all the details then you keep asking them model name, model year and the specific problem.
                   4. your tone is polite.
                   5. try to use maximum 20 words in a response and explain with step by step or bullet point .
                   6. if user is just greeting then only respond "Hello, How can I assist you today?"
                   7. you have previous history also in {history}
            user quesion: {input}
            """
        )
        memory=ConversationBufferMemory()
        st.session_state['conversation']=ConversationChain(
            llm=llm,
            memory=memory,
            prompt=prompt,
            verbose=True
        )    
    result=st.session_state['conversation'].predict(input=user_input)
    print(result)
    return result



# UI 
    
st.set_page_config(page_title='Chatbot',page_icon=':robot_face:')
st.markdown("<h1 style='text-align=center;'>How can I assist you today?</h1>",unsafe_allow_html=True)
response_container = st.container()
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("Your question goes here:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')
        if submit_button:
            st.session_state['messages'].append(user_input)
            model_response=get_response(user_input)
            st.session_state['messages'].append(model_response)
            with response_container:
                for i in range(len(st.session_state['messages'])):
                        if (i % 2) == 0:
                            message(st.session_state['messages'][i], is_user=True, key=str(i) + '_user')
                        else:
                            message(st.session_state['messages'][i], key=str(i) + '_AI')