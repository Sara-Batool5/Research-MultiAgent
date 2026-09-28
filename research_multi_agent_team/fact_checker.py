from crewai import Agent
from tools import web_search, verify_source_url

def create_fact_checker(llm):
    return Agent(
        role="Fact Checker",
        goal="Audit key claims and references, flag unsupported statements, and check source availability.",
        backstory="You are a skeptical evidence auditor. Do not claim that a URL check proves a claim. Match claims to source evidence and clearly flag uncertainty.",
        llm=llm, tools=[web_search, verify_source_url], verbose=True, allow_delegation=False,
    )
