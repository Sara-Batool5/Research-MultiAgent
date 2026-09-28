from crewai import Crew, Task, Process
from llm import get_llm
from planner import create_planner
from researcher import create_researcher
from analyst import create_analyst
from fact_checker import create_fact_checker
from report_writer import create_report_writer

AGENT_NAMES = [
    "Research Planner", "Web Researcher", "Evidence Analyst",
    "Fact Checker", "Research Report Writer"
]

def run_research(topic, depth, timeframe, report_length, status):
    llm = get_llm()
    planner = create_planner(llm)
    researcher = create_researcher(llm)
    analyst = create_analyst(llm)
    checker = create_fact_checker(llm)
    writer = create_report_writer(llm)

    inputs = {
        "topic": topic,
        "depth": depth,
        "timeframe": timeframe,
        "report_length": report_length,
    }

    def task_callback(task_output):
        # CrewAI task callbacks run when a task finishes.
        description = str(getattr(task_output, "description", "")).lower()
        completed_name = None
        for name in AGENT_NAMES:
            if name.lower() in description:
                completed_name = name
        if completed_name and completed_name not in status["completed"]:
            status["completed"].append(completed_name)
        idx = len(status["completed"])
        status["active"] = AGENT_NAMES[idx] if idx < len(AGENT_NAMES) else None

    plan_task = Task(
        description="""Create a research plan for: {topic}
Research depth: {depth}; source timeframe: {timeframe}.
Provide 4-7 subquestions, search queries, source-quality criteria, and scope boundaries.
Use the web search tool to test useful search phrases.""",
        expected_output="A focused research plan with subquestions, search queries, and source criteria.",
        agent=planner, callback=task_callback,
    )
    research_task = Task(
        description="""Using the research plan and topic {topic}, conduct web research.
Respect timeframe {timeframe}. Use web search and retrieve webpages when possible.
Capture key findings with source titles and exact URLs. Prefer primary literature, official
institutions, and reputable journals. Clearly state when source content could not be accessed.
Do not fabricate papers, authors, dates, statistics, or links.""",
        expected_output="Evidence notes with key claims, source titles, URLs, dates, and limitations.",
        agent=researcher, context=[plan_task], callback=task_callback,
    )
    analysis_task = Task(
        description="""Analyze the research notes for {topic}. Compare findings, explain mechanisms
or themes where relevant, identify agreement, conflicts, limitations, and research gaps.
Do not add unsupported facts. Preserve source URLs alongside claims.""",
        expected_output="Evidence synthesis, themes, disagreements, limitations, and research gaps.",
        agent=analyst, context=[plan_task, research_task], callback=task_callback,
    )
    check_task = Task(
        description="""Audit the analysis and research evidence for {topic}. Use search and URL
verification tools to check important references. Flag claims without adequate support,
broken links, uncertain publication details, and conflicts. A responding URL is not proof
that the source supports a claim. Return a clear audit and corrections.""",
        expected_output="Claim/source audit, verified URL status where possible, and flagged issues.",
        agent=checker, context=[research_task, analysis_task], callback=task_callback,
    )
    write_task = Task(
        description="""Write a {report_length} research report about {topic}, using the plan,
research evidence, synthesis, and fact-check audit. Include: title, executive summary,
scope/method, thematic findings, evidence limitations, research gaps, conclusion, and
numbered references with URLs. Clearly label uncertain or unsupported items. Never invent
citations. Source timeframe: {timeframe}. Research depth: {depth}.""",
        expected_output="A polished Markdown research report with source-linked references and limitations.",
        agent=writer, context=[plan_task, research_task, analysis_task, check_task],
        callback=task_callback,
    )

    status["active"] = AGENT_NAMES[0]
    crew = Crew(
        agents=[planner, researcher, analyst, checker, writer],
        tasks=[plan_task, research_task, analysis_task, check_task, write_task],
        process=Process.sequential,
        verbose=True,
    )
    return crew.kickoff(inputs=inputs)
