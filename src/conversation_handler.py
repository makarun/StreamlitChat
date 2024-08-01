import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from src.html_templates import bot_template, user_template


class ConversationHandler:
    def __init__(self):
        self.llm = ChatOpenAI()
        self.memory = ConversationBufferMemory(
            memory_key='chat_history', return_messages=True)

    def create_conversation_chain(self, vectorstore):
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=vectorstore.as_retriever(),
            memory=self.memory
        )

    def handle_user_input(self, user_question):
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history = response['chat_history']
        self.display_chat_history()

    def display_chat_history(self):
        st.session_state.chat_history.reverse()
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
        st.session_state.chat_history.reverse()
