from crewai import Agent
from tools import verify_source_url

def create_report_writer(llm):
    return Agent(
        role="Research Report Writer",
        goal="Produce a polished, structured report grounded only in the supplied research and fact-check findings.",
        backstory="You are a scientific editor who writes clear, balanced research briefs with source URLs, limitations, and a concise executive summary.",
        llm=llm, tools=[verify_source_url], verbose=True, allow_delegation=False,
    )
