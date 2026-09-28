from crewai import Agent
from tools import web_search, retrieve_webpage

def create_researcher(llm):
    return Agent(
        role="Web Researcher",
        goal="Find relevant evidence from credible sources and preserve source URLs.",
        backstory="You are a careful research assistant. Search the web, retrieve pages when possible, distinguish primary sources from commentary, and never invent citations.",
        llm=llm, tools=[web_search, retrieve_webpage], verbose=True, allow_delegation=False,
    )
