import base64
import os
import re
import uuid

import replicate
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage

load_dotenv()
st.set_page_config(layout="wide")
# st.title("Create Game")
instructions = [
    'Number of Players: 2', 'Purse: $100',
    'Hole-by-Hole Betting: Each hole will be played individually, with the winner of each hole earning the pot for that hole.',
    'Ties: In the event of a tie for a hole, the pot will carry over to the next hole, and the players tied will continue to compete for the pot until one player emerges as the winner.',
    'Skins: The number of skins to be played for will be 5. Each skin is worth $10 from the total purse.',
    'Betting: Each player will place an equal bet for each hole, which will be $5 from their total purse.',
    'Winning a Skin: The player who wins a hole will earn the skin for that hole, and the pot will be added to their total earnings.',
    'Minimum Number of Players: 2',
    'Optional Rule: None'
]

st.session_state['game_instructions'] = instructions

# initialize app
def get_game_explore_system_message():
    return '''
        You are a golf betting expert. You know every betting game from skins to lone wolf. You will help the user
        build a list of rules for the game they have described in the prompt. The result should be a list of game rules. 
    '''


def get_instruction_system_message():
    return '''
        You are a betting game instruction writer and a python programming expert. You will read a chat and create a bulleted list of instructions
        for the game described. Dont include any text other than the bullet list.     
    '''



def write_chat_message(container, message):
    with container.chat_message(message['text'].type):
        st.write(message['text'].content)



def generate_response(prompt, system_prompt):
    try:
        # Call Replicate to generate response.
        input = {
            "prompt": prompt,
            "max_new_tokens": 512,
            "system_prompt": system_prompt
            # "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        }

        for event in replicate.run(
            "meta/meta-llama-3-8b-instruct",
            input=input
        ):
            yield str(event)


        # return {'text': AIMessage(output)}
    except Exception as err:
        yield 'Whoops something went wrong...'
        # Could be game describing mode or could be game results mode
        # return {'text': AIMessage('Whoops something went wrong...')}

left, right = st.columns([2, 1], vertical_alignment="bottom")
with left:
    st.header("Game Rules", divider="gray")

instuction_col, chat_col = st.columns([2, 1], vertical_alignment="top")
with st.container():
    with instuction_col:
        rule_container = st.container(height=600, border=False)
        with rule_container:
            if 'game_instructions' in st.session_state:
                # for rule in st.session_state['game_instructions']:
                #     st.write(f'{rule}')
                for i, instruction in enumerate(st.session_state['game_instructions']):
                    with st.container(border=True):
                        # st.write(f"{i + 1}. {instruction}")
                        col1, col2, col3 = st.columns([8,1,1])
                        with col1:
                            st.write(f"{instruction}")
                        with col2:
                            if st.button("✏️", key=f"edit_{i}", type="secondary"):
                                st.session_state['game_instructions'][i] = st.text_input(f"Edit instruction {i + 1}",
                                                                                      value=instruction)
                        with col3:
                            if st.button("🗑️", key=f"delete_{i}", type="primary"):
                                st.session_state['game_instructions'].pop(i)

    with chat_col:
        dialog_container = st.container(height=600)
        with dialog_container:
            if 'chat_messages' not in st.session_state:
                starting_message = 'Welcome to GoBet! I can help you automatically reconcile your bets based on the game you describe. What game are you playing today?'

                # message_container.chat_message("ai").write(message_for_chat)
                st.session_state['chat_messages'] = [{'text': AIMessage(starting_message)}]

            for msg in st.session_state.chat_messages:
                write_chat_message(container=dialog_container, message=msg)


                                # st.experimental_rerun()

        # if st.button("Add Instruction"):
        #     st.session_state['game_instructions'].append("")
        #     # st.experimental_rerun()
        #
        # if st.button("Save Game"):
        #     # Here you would implement the logic to save the game instructions
        #     st.success("Game saved successfully!")


if prompt := st.chat_input():

    # Add user input to chat messages
    user_input_message = {'text': HumanMessage(prompt)}
    write_chat_message(container=dialog_container, message=user_input_message)
    st.session_state['chat_messages'].append(user_input_message)

    # generate response for user input
    # with st.chat_message('ai'):
        # response = generate_response(prompt=prompt, system_prompt=get_game_explore_system_message())
        # full_response = st.write_stream(response)
        #
        # instruction_response = generate_response(prompt=full_response, system_prompt=get_instruction_system_message())
        # # print(instruction_response)
        # # print(''.join(str(item) for item in instruction_response))
        # full_instruction_response = ''.join(str(item) for item in instruction_response)
        # lines = full_instruction_response.split('\n')
        # full_instruction_response_list = [line.strip('• ') for line in lines if line.strip()]
        # print(full_instruction_response_list)
        #
        # st.session_state['chat_messages'].append({'text': AIMessage(full_response)})
        # st.session_state['game_instructions'] = full_instruction_response_list
        # st.rerun()

