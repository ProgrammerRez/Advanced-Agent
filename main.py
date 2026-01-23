import streamlit as st
from dotenv import load_dotenv
from typing import Literal

from search_agent import create_graph_agent, main
from langchain_groq import ChatGroq
from langchain_classic.memory.buffer import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate


# =========================
# SETUP
# =========================

load_dotenv()

st.set_page_config(
    page_title="Deep Research Agent Demo",
    initial_sidebar_state="expanded",
    layout="centered"
)

st.title("Deep Research Agent Demo")
st.divider()


# =========================
# SESSION STATE INIT
# =========================

if "llm" not in st.session_state:
    st.session_state.llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3
    )

if "research_agent" not in st.session_state:
    st.session_state.research_agent = create_graph_agent()

if "artifact" not in st.session_state:
    st.session_state.artifact = None

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )


# =========================
# CONVERSATION PROMPT
# =========================

conversation_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You answer questions ONLY using the provided research artifact.\n"
        "Chat history is ONLY for resolving references like 'this', 'that', or 'earlier'.\n"
        "If the answer is NOT explicitly present in the artifact, respond with:\n"
        "'This information is not present in the research findings.'\n"
        "Do NOT infer, guess, or add new facts."
    ),
    (
        "human",
        "Research Artifact:\n{artifact}\n\n"
        "Chat History:\n{chat_history}\n\n"
        "User Question:\n{question}"
    )
])

conversation_chain = conversation_prompt | st.session_state.llm


# =========================
# CONVERSATION FUNCTION
# =========================

def chat_about_report(user_question: str) -> str:
    artifact = st.session_state.artifact

    if artifact is None:
        return "No research artifact is available yet. Please run a research query first."

    history = st.session_state.memory.load_memory_variables({})["chat_history"]

    response = conversation_chain.invoke({
        "artifact": artifact,
        "chat_history": history,
        "question": user_question
    })

    st.session_state.memory.save_context(
        {"question": user_question},
        {"answer": response.content}
    )

    return response.content


# =========================
# RESEARCH INPUT (SIDEBAR)
# =========================

with st.sidebar:
    st.subheader("Run Research")

    topic = st.text_input("Research topic")
    mode: Literal["shallow", "deep"] = st.selectbox(
        "Depth",
        ["shallow", "deep"]
    )

    if st.button("Run Research"):
        if not topic:
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Running research agent..."):
                state = {
                    "topic": topic,
                    "mode": mode
                }

                result = main(query= state['topic'], mode = state['mode'])

                # 🔒 Freeze the artifact
                st.session_state.artifact = result

                # Reset memory when new research runs
                st.session_state.memory.clear()

            st.success("Research completed and artifact stored.")


# =========================
# CHAT UI
# =========================

st.subheader("Ask questions about the research")
