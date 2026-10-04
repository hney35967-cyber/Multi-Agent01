import os
import streamlit as st
from agents import run_nexusfind_engine

# Page Configuration
st.set_page_config(
    page_title="NexusFind AI",
    page_icon="🔍",
    layout="wide"
)

# Header Section
st.title("🔍 NexusFind AI")
st.subheader("Autonomous Multi-Agent Deep Search & Answer Engine")
st.caption("Powered by Groq & CrewAI | Real-time Search with Inline Citations")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Check for Groq API Key from Streamlit Secrets or Manual Input
    api_key_env = st.secrets.get("GROQ_API_KEY", "") or os.environ.get("GROQ_API_KEY", "")
    
    if not api_key_env:
        user_groq_key = st.text_input("Enter Groq API Key:", type="password")
        if user_groq_key:
            os.environ["GROQ_API_KEY"] = user_groq_key
            st.success("API Key set successfully!")
    else:
        os.environ["GROQ_API_KEY"] = api_key_env
        st.success("Groq API Key detected from Environment/Secrets.")

    st.markdown("---")
    st.markdown("### 🤖 Agents at Work")
    st.markdown("1. **Search Planner:** Expands query into search terms.")
    st.markdown("2. **Web Retriever:** Fetches real-time web snippets.")
    st.markdown("3. **Synthesizer:** Writes structured response with citations.")

# Main Query Section
user_query = st.text_input("What would you like to search for?", placeholder="e.g., Latest features in Groq Llama 3 models")

if st.button("Search & Analyze", type="primary"):
    if not os.environ.get("GROQ_API_KEY"):
        st.error("Please provide a valid Groq API Key in the sidebar or Streamlit Secrets!")
    elif not user_query.strip():
        st.warning("Please enter a valid search query.")
    else:
        with st.spinner("🤖 Multi-agents are searching, reading, and synthesizing facts..."):
            try:
                # Run the backend agent engine
                response = run_nexusfind_engine(user_query)
                
                st.markdown("---")
                st.markdown("### 📝 Answer & Verified Sources")
                st.markdown(response)
                
            except Exception as e:
                st.error(f"An error occurred while running agents: {str(e)}")
