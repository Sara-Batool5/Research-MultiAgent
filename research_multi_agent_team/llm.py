import os
import streamlit as st
from crewai import LLM

def get_llm():
    key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
    if not key:
        raise ValueError("GROQ_API_KEY is missing. Add it to Streamlit Secrets.")
    os.environ["GROQ_API_KEY"] = key
    return LLM(
        model="groq/openai/gpt-oss-120b",
        api_key=key,
        temperature=0.2,
    )
