"""
ReviewMate - Streamlit frontend

This will render the structured output produced by the Bob 2.0 subagents
(security, test coverage, complexity, synthesis) for a given PR/diff.

For now this is a placeholder - paste/plug in real subagent output once
you've run it through Bob IDE against sample-repo/.

Run with:
    streamlit run src/app.py
"""

import streamlit as st

st.set_page_config(page_title="ReviewMate", layout="wide")

st.title("ReviewMate")
st.caption("Intelligent Code Review & Quality Coach — built on IBM Bob 2.0")

st.info("Paste or load your Bob subagent output below to see the review.")

# TODO: replace with real output from Bob subagent runs
placeholder_findings = {
    "security": [],
    "test_coverage": [],
    "complexity": [],
    "summary": "Run the Bob subagents first, then plug their output in here.",
}

st.subheader("Security Findings")
st.write(placeholder_findings["security"] or "No findings yet.")

st.subheader("Test Coverage Gaps")
st.write(placeholder_findings["test_coverage"] or "No findings yet.")

st.subheader("Complexity / Style Issues")
st.write(placeholder_findings["complexity"] or "No findings yet.")

st.subheader("Review Summary")
st.write(placeholder_findings["summary"])
