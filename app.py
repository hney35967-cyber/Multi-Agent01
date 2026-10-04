import os
import streamlit as st
from crewai import Crew, Process, Task
from agents import create_agents

# Page Configuration
st.set_page_config(
    page_title="NexusFind AI - Multi-Agent Search Engine",
    page_icon="🔍",
    layout="wide"
)

# Title & Description
st.title("🔍 NexusFind AI")
st.caption("Powered by Google Gemini & CrewAI Multi-Agent Architecture")

# Streamlit Secrets / Environment Variable Setup
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

# API Key Validation
if not os.environ.get("GEMINI_API_KEY"):
    st.error("🔑 GEMINI_API_KEY nahi mili! Kripya Streamlit Secrets mein API key add karein.")
    st.stop()

# User Input
user_query = st.text_input(
    "Aap kya search karna chahte hain?",
    placeholder="e.g., Impact of Agentic AI workflows on enterprise SaaS software..."
)

if st.button("Run Research 🚀", type="primary"):
    if not user_query.strip():
        st.warning("Kripya search query enter karein.")
    else:
        try:
            with st.spinner("Multi-Agent Engine runs ho raha hai... (Planner → Retriever → Synthesizer)"):
                # Initialize Gemini Agents
                planner, retriever, synthesizer = create_agents()

                # Define Tasks
                task_plan = Task(
                    description=f"Analyze the user query: '{user_query}'. Break it down into clear, high-intent web search strategies.",
                    expected_output="A structured search plan with target keywords.",
                    agent=planner
                )

                task_retrieve = Task(
                    description="Execute the planned web search strategy using DuckDuckGo. Gather live data, facts, statistics, and source URLs.",
                    expected_output="Raw collected web data with exact URLs.",
                    agent=retriever
                )

                task_synthesize = Task(
                    description="Synthesize the collected data into a clean, structured report. Include inline bracketed citations like [1], [2] and list clickable source URLs at the end under '### Sources'.",
                    expected_output="A polished Markdown report with inline citations and a sources list.",
                    agent=synthesizer
                )

                # Assemble Crew
                nexus_crew = Crew(
                    agents=[planner, retriever, synthesizer],
                    tasks=[task_plan, task_retrieve, task_synthesize],
                    process=Process.sequential,
                    verbose=True
                )

                # Execute
                result = nexus_crew.kickoff()

            st.success("Research Complete!")
            st.markdown("### 📊 Research Report")
            st.markdown(str(result))

        except Exception as e:
            st.error(f"An error occurred while running agents: {str(e)}")
