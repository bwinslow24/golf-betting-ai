import base64
import os
import re
import uuid

import replicate
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from streamlit.components import v1 as components

# from langchain_community.chat_models import ChatPerplexity
# from langchain_core.messages import SystemMessage, trim_messages, HumanMessage, AIMessage
#
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_community.chat_message_histories import ChatMessageHistory, StreamlitChatMessageHistory
#
# from dotenv import load_dotenv
# from templates import topic_selection_template, title_selection_template, story_builder_template
from langchain.chains import LLMChain
from langchain_community.llms import Replicate
from langchain_core.prompts import PromptTemplate

load_dotenv()
st.set_page_config(layout="wide")
st.title("GoBet AI")


# initialize app
def get_system_message():
    return '''
        You are a golf betting expert. You know every betting game from skins to lone wolf. You will help the user
        build a list of rules for the game they have described in the prompt. The result should be a list of game rules
    '''


def write_chat_message(container, message):
    with container.chat_message(message['text'].type):
        st.write(message['text'].content)


def generate_response(prompt):
    try:
        # Call Replicate to generate response.
        input = {
            "prompt": prompt,
            "max_new_tokens": 512,
            "system_prompt": get_system_message()
            # "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        }

        for event in replicate.run(
            "meta/meta-llama-3-8b-instruct",
            input=input
        ):
            yield event


        # return {'text': AIMessage(output)}
    except Exception as err:
        yield 'Whoops something went wrong...'
        # Could be game describing mode or could be game results mode
        # return {'text': AIMessage('Whoops something went wrong...')}


chat_col, story_col = st.columns(2)
# React to user input
with chat_col:
    with st.container(height=500):
        message_container = st.container(height=400)
        if 'chat_messages' not in st.session_state:
            starting_message = 'Welcome to GoBet! I can help you automatically reconcile your bets based on the game you describe. What game are you playing today?'

            # message_container.chat_message("ai").write(message_for_chat)
            st.session_state['chat_messages'] = [{'text': AIMessage(starting_message)}]

        for msg in st.session_state.chat_messages:
            write_chat_message(container=message_container, message=msg)

        if prompt := st.chat_input():
            # Add user input to chat messages
            user_input_message = {'text': HumanMessage(prompt)}
            write_chat_message(container=message_container, message=user_input_message)

            st.session_state['chat_messages'].append(user_input_message)
            # generate response for user input
            with message_container.chat_message('ai'):
                response = generate_response(prompt=prompt)
                st.write_stream(response)

            st.session_state['chat_messages'].append({'text': AIMessage(prompt)})
            # write_chat_message(container=message_container, message=response)
