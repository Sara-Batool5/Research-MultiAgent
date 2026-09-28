from crewai import Agent
from tools import retrieve_webpage

def create_analyst(llm):
    return Agent(
        role="Evidence Analyst",
        goal="Synthesize retrieved evidence, compare findings, and identify limitations and research gaps.",
        backstory="You are an analytical researcher who distinguishes established findings, emerging evidence, disagreement, and unanswered questions.",
        llm=llm, tools=[retrieve_webpage], verbose=True, allow_delegation=False,
    )
