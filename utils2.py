import os
import warnings
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.llms.cohere import Cohere

warnings.filterwarnings("ignore")

# Initialize Cohere API key (you should set it as an environment variable)
os.environ['COHERE_API_KEY'] = 'd7TP509U4vjmFcXmxQD0YFizCOeXBaZzq3K77SFs'

def get_response(user_input):
    # Initialize session state for conversation
    if 'conversation' not in st.session_state or st.session_state['conversation'] is None:
        llm = Cohere(temperature=0.7)
        
        # Define the prompt template
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
        
        # Create the LLMChain with conversation memory
        memory = ConversationBufferMemory()
        st.session_state['conversation'] = ConversationChain(llm=llm, prompt=prompt, memory=memory, verbose=True)

    # Predict the response
    result = st.session_state['conversation'].predict(input=user_input)
    print('result')
    return result
