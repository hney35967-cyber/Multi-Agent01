import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.tools import tool
from duckduckgo_search import DDGS
from crewai import LLM

def get_groq_llm():
    api_key = os.environ.get("GROQ_API_KEY")
    return LLM(
        model="groq/llama-3.3-70b-versatile",  # 'groq/' prefix zaroori hai
        api_key=api_key,
        temperature=0.2
    )
# -------------------------------------------------------------------
# Custom Search Tool
# -------------------------------------------------------------------
@tool("DuckDuckGo Web Search")
def web_search_tool(query: str) -> str:
    """Searches the web using DuckDuckGo and returns top snippets with titles and URLs."""
    try:
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=4))
        if not results:
            return "No relevant search results found."

        formatted_results = []
        for idx, res in enumerate(results, start=1):
            title = res.get("title", "No Title")
            url = res.get("href", "#")
            snippet = res.get("body", "")
            formatted_results.append(
                f"Source [{idx}]:\nTitle: {title}\nURL: {url}\nSnippet: {snippet}\n"
            )

        return "\n---\n".join(formatted_results)
    except Exception as e:
        return f"Error executing web search: {str(e)}"

# -------------------------------------------------------------------
# Engine Function
# -------------------------------------------------------------------
def run_nexusfind_engine(user_query: str) -> str:
    # Get Groq LLM instance
    llm = get_groq_llm()

    # Agent 1: Search Planner
    search_planner = Agent(
        role="Search Strategy Specialist",
        goal="Deconstruct complex user queries into 2 to 3 distinct, targeted search phrases.",
        backstory="You are an expert at information retrieval strategy. Generate optimal search queries.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    # Agent 2: Web Retriever
    web_retriever = Agent(
        role="Information Verification Specialist",
        goal="Execute search queries using web search tool and extract accurate snippets.",
        backstory="You are a factual verifier extracting textual snippets with metadata.",
        tools=[web_search_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    # Agent 3: Synthesizer & Citer
    synthesizer = Agent(
        role="Lead Technical Writer & Editor",
        goal="Synthesize extracted facts into a clear answer with inline bracketed citations [1], [2].",
        backstory="You synthesize facts into clean Markdown. Always include inline numeric citations.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    # Tasks
    plan_task = Task(
        description=f"Analyze query: '{user_query}'. Generate 2-3 specific search queries.",
        expected_output="List of search queries.",
        agent=search_planner,
    )

    retrieve_task = Task(
        description="Search DuckDuckGo using generated queries and collect snippets with URLs.",
        expected_output="Structured web search snippets.",
        agent=web_retriever,
    )

    synthesis_task = Task(
        description=(
            f"Synthesize web information for query: '{user_query}'.\n"
            "Include inline numeric citations like [1], [2] and a '### Sources' section at the end."
        ),
        expected_output="Markdown response with citations and Sources list.",
        agent=synthesizer,
    )

    crew = Crew(
        agents=[search_planner, web_retriever, synthesizer],
        tasks=[plan_task, retrieve_task, synthesis_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    return str(result)
