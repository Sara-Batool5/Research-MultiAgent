import os
import streamlit as st
from crewai import LLM


def get_llm():
    api_key = st.secrets.get(
        "GROQ_API_KEY",
        os.getenv("GROQ_API_KEY")
    )

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing.")

    return LLM(
        model="groq/openai/gpt-oss-120b",
        api_key=api_key,
        temperature=0.2,
        max_tokens=2048,
    )
