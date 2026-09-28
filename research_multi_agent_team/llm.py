
import os
import streamlit as st
from crewai import LLM


def get_llm():
    groq_api_key = st.secrets.get(
        "GROQ_API_KEY",
        os.getenv("GROQ_API_KEY")
    )

    if not groq_api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. "
            "Add it in Streamlit Cloud Secrets."
        )

    return LLM(
        model="groq/openai/gpt-oss-120b",
        api_key=groq_api_key,
        temperature=0.2,
        max_tokens=4096,
        extra_params={
            "cache": False
        }
    )
