import streamlit as st
from api_ollama import get_models
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

st.set_page_config(page_title="Marybot", page_icon="👍")

st.title("Marybot :speech_balloon:")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# response from AI

def get_response(query, chat_history, model_option):
    template = """
    You are a helpful assistant. Answer the following questions considering the history fo the conversation,
    if the chat_history is empty, just answer the question being objective:

    Chat history: {chat_history}

    User question: {user_question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOllama(model=model_option, temperature=0)

    chain = prompt | llm | StrOutputParser()

    return chain.stream({
     "chat_history": chat_history,
     "user_question": query   
    })

# chat complete

for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("User"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content) 

# sidebar

with st.sidebar:
    models = get_models()
    st.header("Parâmetros")
    model_option = st.selectbox("Escolha um modelo", models, index=None, placeholder="Disponível no Ollama")
    if model_option is not None:
        st.write("Você escolheu: ", model_option, ":white_check_mark:")

# user 
user_query = st.chat_input("Query here")
if user_query is not None and user_query != "" and model_option is not None:
    st.session_state.chat_history.append(HumanMessage(user_query))

    with st.chat_message("User"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response = st.write_stream(get_response(user_query, st.session_state.chat_history, model_option))
    st.session_state.chat_history.append(AIMessage(ai_response))


