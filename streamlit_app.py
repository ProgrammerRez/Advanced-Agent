import streamlit as st
import requests
import json
import time
import os
from typing import Optional
from dotenv import load_dotenv
import threading
import uvicorn
from app import app

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

api_thread = threading.Thread(target=run_api, daemon=True)
api_thread.start()

load_dotenv()

# Note: Backend should be started separately via 'python app.py' 
# to avoid port conflicts during Streamlit reloads.

# Set page config
st.set_page_config(
    page_title="Advanced Validator AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# CUSTOM STYLING (Antigravity Aesthetic)
# ==========================================
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0D121F;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    
    /* Cyan Accents */
    .cyan-text { color: #06B6D4; }
    .stButton>button {
        background-color: #06B6D4 !important;
        color: #0B0F19 !important;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px rgba(6, 182, 212, 0.4);
        transform: translateY(-1px);
    }
    
    /* Custom containers (Glassmorphism) */
    .glass-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 24px;
        margin-bottom: 20px;
    }
    
    /* Status indicators */
    .status-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        padding: 4px 8px;
        border-radius: 4px;
        text-transform: uppercase;
        font-weight: bold;
    }
    .status-online { background: rgba(16, 185, 129, 0.1); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.2); }
    .status-offline { background: rgba(239, 68, 68, 0.1); color: #EF4444; border: 1px solid rgba(239, 68, 68, 0.2); }
    
    /* Chat bubbles */
    .user-msg {
        background: #06B6D4;
        color: #0B0F19;
        padding: 12px 16px;
        border-radius: 12px 12px 0 12px;
        margin-left: auto;
        max-width: 80%;
        margin-bottom: 15px;
    }
    .bot-msg {
        background: rgba(255, 255, 255, 0.05);
        color: #E2E8F0;
        padding: 12px 16px;
        border-radius: 12px 12px 12px 0;
        margin-right: auto;
        max-width: 80%;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #1E293B; border-radius: 10px; }
    
    /* Code blocks */
    code {
        font-family: 'JetBrains Mono', monospace !important;
        background: rgba(0,0,0,0.3) !important;
        color: #A5F3FC !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR / CONFIG
# ==========================================
with st.sidebar:
    st.markdown("<h2 class='cyan-text'>CORE_VALIDATOR</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("Intelligence depth")
    mode = st.radio(
        "Depth",
        ["shallow", "deep"],
        index=0,
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.subheader("Authentication")
    groq_api_key = os.getenv('GROQ_API_KEY') or st.text_input("Groq API Key (Override)", type="password", placeholder="gsk_...")
    
    st.markdown("---")
    st.subheader("Backend status")
    
    try:
        health_res = requests.get("http://0.0.0.0:8000/health", timeout=2)
        if health_res.status_code == 200:
            st.markdown('<div class="status-badge status-online">● Online</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-badge status-offline">○ Error</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div class="status-badge status-offline">○ Offline</div>', unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.info("v2.0.0 Beta\nValidated Agentic Engine")

# ==========================================
# MAIN APP
# ==========================================
st.markdown("<h1>Intelligence <span class='cyan-text'>Terminal</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748B; margin-top: -15px;'>READY // OMNI_SEARCH_ACTIVE</p>", unsafe_allow_html=True)

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-msg">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        if "data" in message:
            # Result block
            data = message["data"]
            with st.container():
                st.markdown(f'<div class="bot-msg"><b>RESEARCH COMPLETE:</b> {data.get("topic", "Result")}</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns([1.5, 1])
                with col1:
                    st.markdown("### Agent Synthesis")
                    st.write(data.get("final_report", "No report generated."))
                    
                with col2:
                    st.markdown("### Evidence")
                    score = int(data.get("confidence_score", 0) * 100)
                    st.metric("Inference Certainty", f"{score}%")
                    
                    st.markdown("**Validated Sources**")
                    for src in data.get("validated_sources", [])[:5]:
                        st.markdown(f"- [`{src.split('//')[-1][:30]}...`]({src})")
        else:
            st.markdown(f'<div class="bot-msg">{message["content"]}</div>', unsafe_allow_html=True)

# Input area
query = st.chat_input("Type research topic or hypothesis...")

if query:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": query})
    st.rerun()

# Processing the latest user message
if st.session_state.get("messages") and st.session_state.messages[-1]["role"] == "user":
    user_query = st.session_state.messages[-1]["content"]
    
    with st.spinner("Deploying Agents..."):
        try:
            # Prepare payload
            payload = {
                "query": user_query,
                "mode": mode,
                "groq_api_key": groq_api_key if groq_api_key else None
            }
            
            # API Call (with trailing slash and query param for key)
            api_key = os.getenv("RESEARCH_API_KEY", "")
            response = requests.post(
                "http://0.0.0.0:8000/research_agent/",
                params={"api_key": api_key},
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=120
            )
            
            if response.status_code == 200:
                full_data = response.json()
                
                # Extract the synthesize data from the list of events
                research_data = {}
                if isinstance(full_data, list):
                    for event in reversed(full_data):
                        if "synthesize" in event:
                            research_data = event["synthesize"]
                            break
                elif isinstance(full_data, dict):
                    research_data = full_data.get("synthesize", {})
                
                # Store result
                st.session_state.messages.append({
                    "role": "bot",
                    "content": "Analysis Complete.",
                    "data": research_data
                })
                st.rerun()
            else:
                error_data = response.json()
                err_msg = error_data.get("error", {}).get("message", "Unknown Error")
                hint = error_data.get("error", {}).get("hint", "")
                st.error(f"**{err_msg}**\n\n{hint}")
                st.session_state.messages.append({
                    "role": "bot",
                    "content": f"ERROR: {err_msg}. {hint}"
                })
                
        except Exception as e:
            st.error(f"Connection Failed: {str(e)}")
            st.session_state.messages.append({
                "role": "bot",
                "content": f"CONNECTION_FAULT: {str(e)}"
            })
            st.rerun()

# Footer
st.markdown("""
<div style="position: fixed; bottom: 10px; width: 100%; text-align: center; color: #334155; font-size: 10px; font-family: 'JetBrains Mono';">
    ANTIGRAVITY // CORE // 2026
</div>
""", unsafe_allow_html=True)
