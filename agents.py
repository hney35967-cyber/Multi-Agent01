import os
from crewai import Agent, LLM
from crewai_tools import SerperDevTool, DuckDuckGoSearchRun

def get_gemini_llm():
    """
    Initializes and returns the Google Gemini LLM instance via CrewAI / LiteLLM.
    Retrieves GEMINI_API_KEY from environment variables or Streamlit secrets.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing. Please set it in Streamlit Secrets.")

    return LLM(
        model="gemini/gemini-2.5-flash",  # Gemini's high-speed, stable production model
        api_key=api_key,
        temperature=0.2
    )

def create_agents():
    """
    Creates and returns the three core agents for NexusFind AI initialized with Gemini LLM.
    """
    # Initialize Gemini LLM Engine
    gemini_llm = get_gemini_llm()
    
    # Live Web Search Tool
    search_tool = DuckDuckGoSearchRun()

    # 1. Search Planner Agent
    planner = Agent(
        role="Search Strategy Planner",
        goal="Analyze user research queries and break them down into effective, targeted search strategies.",
        backstory=(
            "You are an expert search planner. Your job is to dissect complex user queries "
            "and create concise, high-intent search terms to retrieve accurate real-time data from the web."
        ),
        llm=gemini_llm,
        verbose=True,
        allow_delegation=False
    )

    # 2. Web Retriever Agent
    retriever = Agent(
        role="Real-Time Web Data Retriever",
        goal="Execute planned search queries and gather authentic facts, statistics, and URLs from the internet.",
        backstory=(
            "You are a diligent research assistant equipped with web search capabilities. "
            "You search the web live, gather precise facts, and keep track of source URLs for proper citation."
        ),
        tools=[search_tool],
        llm=gemini_llm,
        verbose=True,
        allow_delegation=False
    )

    # 3. Synthesizer Agent
    synthesizer = Agent(
        role="Research Synthesizer and Citation Specialist",
        goal="Synthesize retrieved web data into a comprehensive report with inline citations and clickable sources.",
        backstory=(
            "You are a professional technical writer and research analyst. "
            "You take raw web search results, organize them into structured Markdown sections, "
            "add bracketed numerical citations like [1], [2], and list source URLs at the end."
        ),
        llm=gemini_llm,
        verbose=True,
        allow_delegation=False
    )

    return planner, retriever, synthesizer
