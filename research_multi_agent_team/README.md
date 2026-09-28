# NEXUS Research Multi-Agent Team

A Streamlit research assistant powered by CrewAI and Groq.

## Features
- Five specialized agents: planner, researcher, analyst, fact checker, report writer
- Web search through Serper
- Webpage retrieval and URL availability checks
- Dark research-dashboard UI with agent status
- Markdown and TXT report downloads

## Secrets
Set these in Streamlit Cloud → App settings → Secrets:

```toml
GROQ_API_KEY = "your_groq_key"
SERPER_API_KEY = "your_serper_key"
```

## Deploy
1. Upload all files to a GitHub repository.
2. In Streamlit Community Cloud, create a new app and select the repository.
3. Set the main file path to `app.py`.
4. Add the secrets above and deploy.

## Notes
Research outputs are AI-generated and should be independently verified. URL availability does not establish the accuracy of a claim.
