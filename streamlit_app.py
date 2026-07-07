import json
import os
import subprocess
import sys

import streamlit as st

st.set_page_config(page_title="Deep Research Agent", page_icon="🔎")
st.title("🔎 Deep Research Agent")
st.caption(
    "Bring your own free API keys. Nothing is stored on this server - your keys are used only "
    "for this one research run and go directly to Google/Groq/Tavily."
)

provider = st.selectbox("LLM Provider", ["google_genai", "groq"])

if provider == "google_genai":
    llm_key = st.text_input(
        "Google AI Studio API Key",
        type="password",
        help="Free, no card required: https://aistudio.google.com/apikey",
    )
else:
    llm_key = st.text_input(
        "Groq API Key",
        type="password",
        help="Free, no card required: https://console.groq.com/keys",
    )

tavily_key = st.text_input(
    "Tavily API Key",
    type="password",
    help="Free, no card required: https://app.tavily.com",
)

query = st.text_area(
    "Research question",
    height=150,
    placeholder="e.g. Compare TSMC and Intel's chip manufacturing strategies for 2026-2028",
)

if st.button("Run Research", type="primary"):
    if not llm_key or not tavily_key or not query.strip():
        st.error("Please fill in your API key(s) and a research question.")
    else:
        env = os.environ.copy()
        env["LLM_PROVIDER"] = provider
        env["TAVILY_API_KEY"] = tavily_key
        if provider == "google_genai":
            env["GOOGLE_API_KEY"] = llm_key
        else:
            env["GROQ_API_KEY"] = llm_key

        with st.spinner("Researching... this can take a few minutes for a deep query."):
            try:
                result = subprocess.run(
                    [sys.executable, "worker.py"],
                    input=query,
                    capture_output=True,
                    text=True,
                    env=env,
                    timeout=900,
                )
            except subprocess.TimeoutExpired:
                st.error("Research run timed out after 15 minutes. Try a narrower question.")
                result = None

        if result is not None:
            if result.returncode != 0:
                st.error(f"Research failed:\n\n{result.stderr[-2000:]}")
            else:
                output = json.loads(result.stdout.strip().splitlines()[-1])
                if "error" in output:
                    st.error(output["error"])
                else:
                    st.markdown(output["final_report"])
