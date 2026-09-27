"""
ReviewMate - Streamlit frontend
Built on IBM Bob 2.0 | IBM Bob 2.0 Hackathon 2026

Loads docs/sample-findings.json (produced by running Bob IDE subagents
against sample-repo/) and renders it as a readable, modern PR review report.

Run with:
    python -m streamlit run src/app.py
"""

import json
import os
import streamlit as st

# ---------- Config ----------
st.set_page_config(page_title="ReviewMate", page_icon="🔍", layout="wide")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "docs", "sample-findings.json")
REPORT_PATH = os.path.join(os.path.dirname(__file__), "..", "docs", "pr-review-sample-report.html")

RECOMMENDATION_STYLE = {
    "approve": ("APPROVE", "#0f2e1a", "#3fb950", "#1a7f37"),
    "approve_with_comments": ("APPROVE WITH COMMENTS", "#332600", "#e3b341", "#9e6a03"),
    "request_changes": ("REQUEST CHANGES", "#3d1418", "#f85149", "#da3633"),
}

SEVERITY_COLOR = {
    "high": "#f85149",
    "medium": "#e3b341",
    "low": "#58a6ff",
}

# ---------- Global CSS ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', -apple-system, sans-serif;
    }

    .block-container {
        padding-top: 2.5rem;
        max-width: 1000px;
    }

    .rm-hero {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 4px;
    }
    .rm-hero h1 {
        font-size: 40px;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(90deg, #58a6ff, #a371f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .rm-subtitle {
        color: #8b949e;
        font-size: 15px;
        margin-bottom: 28px;
    }

    .rm-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 18px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 13px;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        border: 1px solid;
        margin-bottom: 4px;
    }

    .rm-overview {
        color: #c9d1d9;
        font-size: 15px;
        line-height: 1.6;
        margin-top: 14px;
    }

    .rm-metric-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin: 28px 0;
    }
    .rm-metric {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 18px 20px;
    }
    .rm-metric .num {
        font-size: 28px;
        font-weight: 800;
        color: #f0f6fc;
    }
    .rm-metric .label {
        font-size: 12px;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-top: 2px;
    }

    .rm-section-title {
        font-size: 20px;
        font-weight: 700;
        color: #f0f6fc;
        margin: 36px 0 14px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .rm-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-left: 4px solid var(--sev-color, #30363d);
        border-radius: 8px;
        padding: 16px 18px;
        margin-bottom: 12px;
    }
    .rm-card-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 6px;
    }
    .rm-card-title {
        font-weight: 700;
        font-size: 14.5px;
        color: #f0f6fc;
    }
    .rm-sev-pill {
        font-size: 10.5px;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 999px;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        white-space: nowrap;
    }
    .rm-card-meta {
        font-size: 12px;
        color: #8b949e;
        margin-bottom: 8px;
        font-family: 'SFMono-Regular', Consolas, monospace;
    }
    .rm-card-body {
        font-size: 13.5px;
        color: #c9d1d9;
        line-height: 1.5;
    }

    .rm-top-finding {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 8px;
        font-size: 14px;
        color: #c9d1d9;
        display: flex;
        gap: 10px;
    }
    .rm-top-finding .rank {
        font-weight: 800;
        color: #58a6ff;
        min-width: 20px;
    }

    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


def load_findings():
    with open(DATA_PATH, "r") as f:
        return json.load(f)


# ---------- Load data ----------
try:
    data = load_findings()
except FileNotFoundError:
    st.error(f"Could not find {DATA_PATH}. Make sure docs/sample-findings.json exists.")
    st.stop()

security = data.get("security", [])
test_coverage = data.get("test_coverage", [])
complexity = data.get("complexity", [])
summary = data.get("summary", {})

coverage_gap_count = sum(
    1 for t in test_coverage
    if t.get("suggested_tests")
)

# ---------- Hero ----------
st.markdown(
    """
    <div class="rm-hero">
        <h1>🔍 ReviewMate</h1>
    </div>
    <div class="rm-subtitle">Intelligent Code Review & Quality Coach — built on IBM Bob 2.0</div>
    """,
    unsafe_allow_html=True,
)

rec_key = summary.get("recommendation", "approve_with_comments")
rec_label, rec_bg, rec_border, rec_dot = RECOMMENDATION_STYLE.get(
    rec_key, RECOMMENDATION_STYLE["approve_with_comments"]
)

st.markdown(
    f"""
    <div class="rm-badge" style="background:{rec_bg};color:{rec_border};border-color:{rec_border}55;">
        ● {rec_label}
    </div>
    <div class="rm-overview">{summary.get("overview", "")}</div>
    """,
    unsafe_allow_html=True,
)

# ---------- Metrics ----------
st.markdown(
    f"""
    <div class="rm-metric-row">
        <div class="rm-metric"><div class="num">{len(security)}</div><div class="label">Security findings</div></div>
        <div class="rm-metric"><div class="num">{coverage_gap_count}</div><div class="label">Coverage gaps</div></div>
        <div class="rm-metric"><div class="num">{len(complexity)}</div><div class="label">Quality issues</div></div>
        <div class="rm-metric"><div class="num">{summary.get('estimated_time_saved_minutes', '—')}m</div><div class="label">Time saved</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Top findings ----------
st.markdown('<div class="rm-section-title">🏆 Top Findings</div>', unsafe_allow_html=True)
for i, f in enumerate(summary.get("top_findings", []), start=1):
    st.markdown(
        f'<div class="rm-top-finding"><span class="rank">#{i}</span><span>{f}</span></div>',
        unsafe_allow_html=True,
    )

if summary.get("reasoning"):
    with st.expander("Why this recommendation?"):
        st.write(summary["reasoning"])

# ---------- Security ----------
st.markdown(f'<div class="rm-section-title">🔐 Security Findings ({len(security)})</div>', unsafe_allow_html=True)
if security:
    for item in security:
        sev = item.get("severity", "low")
        color = SEVERITY_COLOR.get(sev, "#30363d")
        meta = item.get("file", "")
        if item.get("line"):
            meta += f" · line {item.get('line')}"
        st.markdown(
            f"""
            <div class="rm-card" style="--sev-color:{color};">
                <div class="rm-card-top">
                    <span class="rm-card-title">{item.get('risk', 'Finding')}</span>
                    <span class="rm-sev-pill" style="background:{color}22;color:{color};">{sev}</span>
                </div>
                <div class="rm-card-meta">{meta}</div>
                <div class="rm-card-body">{item.get('explanation', '')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.write("No security findings.")

# ---------- Test coverage ----------
st.markdown(f'<div class="rm-section-title">🧪 Test Coverage ({len(test_coverage)})</div>', unsafe_allow_html=True)
if test_coverage:
    for item in test_coverage:
        status = item.get("coverage_status", "")
        with st.expander(f"{item.get('function', 'Function')} — {status}"):
            suggested = item.get("suggested_tests", [])
            if suggested:
                st.write("Suggested tests:")
                for t in suggested:
                    st.markdown(f"- {t}")
            else:
                st.write("Fully covered — no gaps.")
else:
    st.write("No test coverage data.")

# ---------- Complexity ----------
st.markdown(f'<div class="rm-section-title">🧹 Complexity / Style Issues ({len(complexity)})</div>', unsafe_allow_html=True)
if complexity:
    for item in complexity:
        with st.expander(f"{item.get('file', '')} — {item.get('issue', '')[:60]}"):
            st.write(f"**Issue:** {item.get('issue', '')}")
            st.write(f"**Suggested fix:** {item.get('suggested_fix', '')}")
else:
    st.write("No complexity issues.")

# ---------- Full report ----------
if os.path.exists(REPORT_PATH):
    with open(REPORT_PATH, "r") as f:
        report_html = f.read()
    st.markdown('<div class="rm-section-title">📄 Full Bob-Generated Report</div>', unsafe_allow_html=True)
    st.caption("The complete PR review report generated directly by the Bob synthesis subagent.")
    with st.expander("View full report"):
        st.components.v1.html(report_html, height=900, scrolling=True)
    st.download_button(
        "⬇ Download full report (HTML)",
        data=report_html,
        file_name="pr-review-sample-report.html",
        mime="text/html",
    )

st.markdown(
    "<div style='text-align:center;color:#484f58;font-size:12px;margin-top:40px;'>"
    "Built with IBM Bob 2.0 · ReviewMate — IBM Bob 2.0 Hackathon 2026</div>",
    unsafe_allow_html=True,
)