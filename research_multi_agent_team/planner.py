from crewai import Agent
from tools import web_search

def create_planner(llm):
    return Agent(
        role="Research Planner",
        goal="Convert the user's research question into a focused, practical research plan.",
        backstory="You are a methodical research strategist who defines scope, subquestions, search terms, and inclusion criteria.",
        llm=llm, tools=[web_search], verbose=True, allow_delegation=False,
    )
