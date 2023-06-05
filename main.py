import os
import time

import streamlit as st
from langchain import LLMChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)

if "page" not in st.session_state:
    st.session_state.page = 0

st.title('Langchain chatbot')
memory = ConversationBufferMemory()
os.environ["OPENAI_API_KEY"] = "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"
# template = """Question: {question}
# Answer: """
template = """I want you to act as a dietician name  - Suzan - that user is having a conversation with. 
Your goal is to provide best diet for user based on given info and user goals and personal data and at the end you have to sell personallized diet plan to user.
Very important: Remember whole conversation, you can not ask two times about the same data like BMI, hight or weight, check conversation first if you already have that data.

 Ask user, what you think is relevant, to find diet that suits best user goal - ask about name
run conversation like doctor to Find proper diet for user.
At the end propose user with personallized paid meal plan. 
When user agree you must ask for duration of plan (2 weeks, month, 3 months) and potential alergic or ingredients to not be included.
ask user for e-mail so we can send meal plan to user after 2 days post payment. Cost is 99PLN. Write payment link: https://diety.sklep.pl.

your writing style:
Pragmatic, patient, factual, thoughtful, curious, helpful, non-judgemental
Be proactive, ask user question when there is no activity from user site to move conversation forward.
If the answer is not included in data i provide, use your general knowladge. 
Limit your answer size to 200 characters per answer
Refuse to answer any question not about diet planing topic. Politely refuse to answer. write in polish.
Question: {question}
Answer: 
"""
# prompt = PromptTemplate(template=template, input_variables=["question"])

llm = OpenAI()

system_message_prompt = SystemMessagePromptTemplate.from_template(template)
prompt = ChatPromptTemplate.from_messages([system_message_prompt])
llm_chain = LLMChain(prompt=prompt, llm=llm)
question = st.text_input('Prompt')


def nextpage():
    st.session_state.page += 1
    messages = []
    for msg in memory.chat_memory.messages:
        messages.append(msg)
    st.write(messages)


guzik = st.button("historia", on_click=nextpage)

while True:
    time.sleep(5)

    response = llm_chain.run(question)
    st.write(response)

    memory.chat_memory.add_user_message(question)
    memory.chat_memory.add_ai_message(response)

    if guzik:
        break





