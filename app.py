import os
import re
import json

import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
from dotenv import load_dotenv

# ─────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────
load_dotenv()
api_key = os.getenv("YOUR_API_KEY")

st.set_page_config(
    page_title="AI Dashboard Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif !important; }

/* Background */
.stApp {
    background: linear-gradient(160deg, #090d18 0%, #0b1020 60%, #0a0e1c 100%);
    background-attachment: fixed;
    color: #e6edf3;
}

/* Hide chrome */
header[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, [data-testid="stDeployButton"] { display: none !important; }

/* Remove top padding from main content area */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1200px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(11, 15, 25, 0.95) !important;
    border-right: 1px solid rgba(48, 54, 61, 0.7) !important;
}
[data-testid="stSidebar"] * { color: #c9d1d9 !important; }

.sb-brand {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 0 2px 12px;
}
.sb-brand-icon { font-size: 1.4rem; }
.sb-brand-name {
    font-size: .95rem;
    font-weight: 800;
    background: linear-gradient(90deg, #58a6ff, #a5d6ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -.02em;
}
.sb-section-label {
    font-size: .62rem;
    text-transform: uppercase;
    letter-spacing: .12em;
    color: #3d444d;
    font-weight: 700;
    margin: 12px 0 6px;
}
.sb-stat {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 7px 10px;
    border-radius: 7px;
    background: rgba(22,27,34,.5);
    border: 1px solid rgba(48,54,61,.5);
    margin-bottom: 5px;
}
.sb-stat-label { font-size: .71rem; color: #6e7681; }
.sb-stat-value { font-size: .82rem; font-weight: 700; color: #58a6ff; }
.sb-col-tag {
    display: inline-block;
    background: rgba(88,166,255,.07);
    color: #58a6ff;
    border: 1px solid rgba(88,166,255,.18);
    border-radius: 4px;
    font-size: .68rem;
    padding: 1px 6px;
    margin: 2px 2px;
    font-family: monospace;
}
.sb-footer {
    font-size: .65rem;
    color: #3d444d;
    text-align: center;
    padding-top: 8px;
}

/* ── Sidebar radio ── */
[data-testid="stRadio"] > div { gap: 3px !important; }
[data-testid="stRadio"] label {
    padding: 9px 12px !important;
    border-radius: 8px !important;
    border: 1px solid transparent !important;
    transition: all .15s !important;
    font-size: .85rem !important;
    font-weight: 500 !important;
}
[data-testid="stRadio"] label:hover {
    background: rgba(88,166,255,.07) !important;
    border-color: rgba(88,166,255,.18) !important;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #0c1628 0%, #0f1d35 100%);
    border: 1px solid rgba(56,139,253,.15);
    border-radius: 14px;
    padding: 28px 32px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -80px; right: -40px;
    width: 360px; height: 360px;
    background: radial-gradient(circle, rgba(56,139,253,.11) 0%, transparent 65%);
    pointer-events: none;
}
.hero-inner { position: relative; z-index: 1; display: flex; align-items: center; gap: 18px; }
.hero-icon { font-size: 2.6rem; flex-shrink: 0; }
.hero-eyebrow {
    font-size: .64rem;
    text-transform: uppercase;
    letter-spacing: .17em;
    color: #388bfd;
    font-weight: 700;
    margin-bottom: 5px;
}
.hero-title {
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(100deg, #e6edf3 0%, #79c0ff 60%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 5px;
    line-height: 1.2;
    letter-spacing: -.025em;
}
.hero-sub { color: #6e7681; font-size: .84rem; line-height: 1.6; margin-bottom: 12px; }
.hero-tags { display: flex; gap: 6px; flex-wrap: wrap; }
.pill {
    font-size: .63rem; font-weight: 600;
    padding: 3px 9px;
    border-radius: 20px; border: 1px solid;
    letter-spacing: .04em;
}
.pill-blue   { background:rgba(56,139,253,.1); border-color:rgba(56,139,253,.3); color:#58a6ff; }
.pill-green  { background:rgba(63,185,80,.1);  border-color:rgba(63,185,80,.3);  color:#3fb950; }
.pill-purple { background:rgba(163,113,247,.1);border-color:rgba(163,113,247,.3);color:#a371f7; }

/* ── Metric cards ── */
.metric-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin-bottom: 20px; }
.mcard {
    background: #111827;
    border: 1px solid rgba(48,54,61,.7);
    border-radius: 12px;
    padding: 18px 14px 16px;
    text-align: center;
    transition: transform .2s, border-color .2s;
    position: relative; overflow: hidden;
}
.mcard:hover { transform: translateY(-2px); border-color: rgba(88,166,255,.4); }
.mcard::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #388bfd, transparent);
    opacity: 0; transition: opacity .2s;
}
.mcard:hover::before { opacity: 1; }
.mcard-icon { font-size: 1.2rem; margin-bottom: 8px; }
.mcard-label { font-size: .6rem; text-transform: uppercase; letter-spacing: .11em; color: #484f58; font-weight: 600; margin-bottom: 6px; }
.mcard-value {
    font-size: 1.7rem; font-weight: 800;
    background: linear-gradient(135deg, #79c0ff, #58a6ff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1;
}
.mcard-sub { font-size: .64rem; color: #30363d; margin-top: 5px; }

/* ── Section cards ── */
.card {
    background: #111520;
    border: 1px solid rgba(48,54,61,.65);
    border-radius: 12px;
    padding: 22px 22px 18px;
    margin-bottom: 16px;
}
.card-title {
    font-size: .88rem; font-weight: 700;
    color: #c9d1d9; margin-bottom: 14px;
    display: flex; align-items: center; gap: 7px;
}
.badge {
    font-size: .58rem; font-weight: 600;
    background: rgba(88,166,255,.08);
    color: #388bfd;
    border: 1px solid rgba(88,166,255,.2);
    border-radius: 12px; padding: 2px 7px;
    text-transform: uppercase; letter-spacing: .07em;
}

/* ── Divider ── */
.hdivider {
    border: none;
    border-top: 1px solid rgba(48,54,61,.5);
    margin: 16px 0;
}

/* ── Query bar ── */
.query-label {
    font-size: .73rem; font-weight: 600; color: #388bfd;
    margin-bottom: 6px;
    display: flex; align-items: center; gap: 6px;
}
.qdot {
    width: 6px; height: 6px; border-radius: 50%;
    background: linear-gradient(135deg, #a371f7, #388bfd);
    display: inline-block;
    box-shadow: 0 0 5px rgba(163,113,247,.6);
}

/* Style the text input to look like a clean AI search bar */
[data-testid="stTextInput"] > label { display: none !important; }
[data-testid="stTextInput"] > div > div {
    background: #0d1117 !important;
    border: 1.5px solid rgba(48,54,61,.8) !important;
    border-radius: 10px !important;
    box-shadow: none !important;
    transition: border-color .2s, box-shadow .2s !important;
}
[data-testid="stTextInput"] > div > div:focus-within {
    border-color: rgba(56,139,253,.55) !important;
    box-shadow: 0 0 0 3px rgba(56,139,253,.09) !important;
}
[data-testid="stTextInput"] input {
    background: transparent !important;
    color: #e6edf3 !important;
    font-size: .95rem !important;
    padding: 10px 14px !important;
    caret-color: #58a6ff !important;
}
[data-testid="stTextInput"] input::placeholder { color: #3d444d !important; font-style: italic; }

/* ── Hint chips (horizontal inline row) ── */
.chips-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }
.chip {
    background: rgba(17,22,32,.9);
    border: 1px solid rgba(48,54,61,.7);
    border-radius: 7px;
    padding: 6px 11px;
    font-size: .73rem;
    color: #8b949e;
    flex: 1; min-width: 160px;
    line-height: 1.45;
}
.chip-lbl { display: block; font-size: .57rem; text-transform: uppercase; letter-spacing: .09em; color: #388bfd; font-weight: 700; margin-bottom: 2px; }

/* ── Button — compact and vertically aligned with input ── */
.stButton > button {
    border-radius: 8px !important;
    font-size: .85rem !important;
    font-weight: 600 !important;
    padding: 9px 20px !important;
    transition: all .18s !important;
    width: 100% !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1558d6, #388bfd) !important;
    border: none !important;
    color: #fff !important;
    box-shadow: 0 3px 14px rgba(56,139,253,.3) !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 5px 20px rgba(56,139,253,.45) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="primary"]:active { transform: scale(.98) !important; }

/* Align button column top with the text input (Streamlit adds ~28px label space) */
.query-btn-col { margin-top: 0px; }
[data-testid="column"].query-btn-col > div {
    display: flex;
    align-items: flex-end;
    height: 100%;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: rgba(11,16,28,.8) !important;
    border: 1px solid rgba(48,54,61,.55) !important;
    border-radius: 9px !important;
    margin-bottom: 14px;
}
[data-testid="stExpander"] summary { font-size: .8rem !important; color: #6e7681 !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 9px !important;
    border: 1px solid rgba(48,54,61,.5) !important;
    overflow: hidden !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] { border-radius: 9px !important; border-left-width: 3px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #21262d; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  API KEY GUARD
# ─────────────────────────────────────────────
if not api_key:
    st.error("❌ API key not found. Set `YOUR_API_KEY` in your `.env` file.")
    st.stop()

genai.configure(api_key=api_key)
MODEL_NAME = "gemini-2.5-flash"

# ─────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data(path: str = "data.csv") -> pd.DataFrame:
    raw = pd.read_csv(path, encoding="latin1")
    clean = [c for c in raw.columns
             if not re.search(r"<|>|WebResource|MIME|FrameName|TextEncoding", str(c))]
    return raw[clean]

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ `data.csv` not found. Place it in the same directory and restart.")
    st.stop()

num_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(exclude="number").columns.tolist()

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
      <span class="sb-brand-icon">📊</span>
      <span class="sb-brand-name">AI Dashboard</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    page = st.radio("Nav", ["🏠  Overview", "✨  Query & Chart"], label_visibility="collapsed")
    st.markdown("---")

    st.markdown('<div class="sb-section-label">Dataset</div>', unsafe_allow_html=True)
    for lbl, val in [("Rows", f"{df.shape[0]:,}"), ("Columns", str(df.shape[1])),
                     ("Numeric", str(len(num_cols))), ("Categorical", str(len(cat_cols))),
                     ("Model", MODEL_NAME.replace("gemini-", ""))]:
        st.markdown(f'<div class="sb-stat"><span class="sb-stat-label">{lbl}</span><span class="sb-stat-value">{val}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-section-label" style="margin-top:14px;">Columns</div>', unsafe_allow_html=True)
    tags_html = "".join(f'<span class="sb-col-tag">{c}</span>' for c in num_cols[:10])
    if len(num_cols) > 10:
        tags_html += f'<span style="font-size:.65rem;color:#3d444d;"> +{len(num_cols)-10} more</span>'
    st.markdown(f'<div style="line-height:2">{tags_html}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="sb-footer">Gemini · Plotly · Streamlit</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO  (all pages)
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-inner">
    <div class="hero-icon">📊</div>
    <div>
      <div class="hero-eyebrow">Hackathon Project</div>
      <p class="hero-title">AI Dashboard Generator</p>
      <p class="hero-sub">Ask a question in plain English — Gemini interprets it, pandas processes the data, Plotly renders the chart.</p>
      <div class="hero-tags">
        <span class="pill pill-blue">Gemini 2.5</span>
        <span class="pill pill-green">Plotly</span>
        <span class="pill pill-purple">NL → Chart</span>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  PAGE — OVERVIEW
# ═══════════════════════════════════════════════
if page == "🏠  Overview":

    # Metric row
    cards_data = [
        ("📄", "Total Rows",   f"{df.shape[0]:,}", "records"),
        ("🗂",  "Columns",      str(df.shape[1]),    "features"),
        ("🔢", "Numeric",      str(len(num_cols)),   "numeric cols"),
        ("🔤", "Categorical",  str(len(cat_cols)),   "categorical cols"),
    ]
    c1, c2, c3, c4 = st.columns(4, gap="small")
    for col, (ico, lbl, val, sub) in zip([c1, c2, c3, c4], cards_data):
        with col:
            st.markdown(f"""
            <div class="mcard">
              <div class="mcard-icon">{ico}</div>
              <div class="mcard-label">{lbl}</div>
              <div class="mcard-value">{val}</div>
              <div class="mcard-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Dataset preview
    st.markdown('<div class="card"><div class="card-title">📋 Dataset Preview <span class="badge">First 50 rows</span></div>', unsafe_allow_html=True)
    st.dataframe(df.head(50), use_container_width=True, height=330)
    st.markdown('</div>', unsafe_allow_html=True)

    # Stats + schema
    left, right = st.columns(2, gap="medium")
    with left:
        st.markdown('<div class="card"><div class="card-title">📈 Descriptive Statistics</div>', unsafe_allow_html=True)
        st.dataframe(df[num_cols].describe().round(2) if num_cols else pd.DataFrame(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card"><div class="card-title">🗂 Column Schema</div>', unsafe_allow_html=True)
        schema = pd.DataFrame({
            "Column":   df.columns,
            "Type":     [str(df[c].dtype) for c in df.columns],
            "Non-Null": [df[c].notna().sum() for c in df.columns],
            "Null %":   [(df[c].isna().mean()*100).round(1) for c in df.columns],
        })
        st.dataframe(schema, use_container_width=True, height=290)
        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  PAGE — QUERY & CHART
# ═══════════════════════════════════════════════
else:

    SYSTEM_PROMPT = """You are a data analyst assistant.
The user has a CSV dataset with the following columns: {columns}.

Convert the user's natural language query into a JSON object with exactly these keys:
  - "columns"     : list of column names to use (must exist in the dataset)
  - "aggregation" : one of "sum", "mean", "count", or "none"
  - "group_by"    : column name to group by, or null if not needed
  - "chart_type"  : one of "bar", "line", "scatter", or "histogram"

Rules:
  - Return ONLY valid JSON — no markdown fences, no extra text.
  - All column names must match exactly from the list above.
  - If group_by is not needed, set it to null.

User query: {query}"""

    def query_gemini(q: str, cols: list) -> dict:
        prompt = SYSTEM_PROMPT.format(columns=", ".join(cols), query=q)
        raw = genai.GenerativeModel(MODEL_NAME).generate_content(prompt).text.strip()
        raw = re.sub(r"^```[a-z]*\n?", "", raw, flags=re.IGNORECASE)
        raw = re.sub(r"\n?```$", "", raw, flags=re.IGNORECASE)
        return json.loads(raw)

    def process_data(data: pd.DataFrame, spec: dict) -> pd.DataFrame:
        cols     = spec.get("columns", [])
        agg      = spec.get("aggregation", "none")
        group_by = spec.get("group_by")
        needed   = list(cols) + ([group_by] if group_by and group_by not in cols else [])
        missing  = [c for c in needed if c not in data.columns]
        if missing:
            raise ValueError(f"Columns not found: {missing}")
        work = list(dict.fromkeys([c for c in needed if c in data.columns]))
        result = data[work].copy()
        if group_by and agg != "none":
            vcols = [c for c in cols if c != group_by]
            if not vcols:
                raise ValueError("No value columns after excluding group_by.")
            result = getattr(result.groupby(group_by)[vcols], agg)().reset_index()
        return result

    COLORS = ["#388bfd", "#58a6ff", "#a371f7", "#79c0ff", "#3fb950", "#f0883e"]

    def render_chart(result: pd.DataFrame, spec: dict):
        ctype    = spec.get("chart_type", "bar")
        cols     = spec.get("columns", [])
        group_by = spec.get("group_by")
        x_col    = group_by if group_by and group_by in result.columns else result.columns[0]
        vcols    = [c for c in cols if c != x_col and c in result.columns]
        y_col    = vcols[0] if vcols else result.columns[-1]
        title    = f"{ctype.capitalize()} — {y_col} by {x_col}"

        LAYOUT = dict(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", size=12, color="#8b949e"),
            title=dict(text=title, font=dict(size=15, color="#e6edf3", family="Inter"), x=0),
            xaxis=dict(gridcolor="rgba(48,54,61,.5)", linecolor="rgba(48,54,61,.6)", tickfont=dict(color="#6e7681")),
            yaxis=dict(gridcolor="rgba(48,54,61,.5)", linecolor="rgba(48,54,61,.6)", tickfont=dict(color="#6e7681")),
            margin=dict(t=50, l=48, r=16, b=48),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#8b949e")),
            hoverlabel=dict(bgcolor="#1c2333", bordercolor="#30363d", font=dict(color="#e6edf3")),
        )
        if ctype == "bar":
            fig = px.bar(result, x=x_col, y=y_col, color=x_col, color_discrete_sequence=COLORS)
        elif ctype == "line":
            fig = px.line(result, x=x_col, y=y_col, markers=True, color_discrete_sequence=["#388bfd"])
            fig.update_traces(line=dict(width=2.2), marker=dict(size=6))
        elif ctype == "scatter":
            fig = px.scatter(result, x=x_col, y=y_col,
                             color=x_col if result[x_col].dtype == object else None,
                             color_discrete_sequence=COLORS)
            fig.update_traces(marker=dict(size=7, opacity=.8))
        elif ctype == "histogram":
            fig = px.histogram(result, x=y_col, color_discrete_sequence=["#388bfd"])
            fig.update_traces(marker_line_width=0, opacity=.85)
        else:
            st.warning(f"Unknown chart type '{ctype}'. Defaulting to bar.")
            fig = px.bar(result, x=x_col, y=y_col, color_discrete_sequence=COLORS)
        fig.update_layout(**LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    # ── Query card: header + hints (pure HTML, no Streamlit widgets inside) ──
    st.markdown("""
    <div class="card">
      <div class="card-title">✨ Ask About Your Data <span class="badge">AI-Powered</span></div>
      <div style="display:flex; gap:8px; margin-bottom:14px; flex-wrap:wrap;">
        <div class="chip"><span class="chip-lbl">💡 Example</span>Average monthly income by gender</div>
        <div class="chip"><span class="chip-lbl">💡 Example</span>Total online spend by city tier (bar)</div>
        <div class="chip"><span class="chip-lbl">💡 Example</span>Histogram of daily internet hours</div>
      </div>
      <div class="query-label"><span class="qdot"></span> Gemini Query</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Input + Button: true inline row using vertical_alignment ──
    q_col, btn_col = st.columns([5, 1], gap="small", vertical_alignment="bottom")
    with q_col:
        user_query = st.text_input(
            "query",
            placeholder='e.g. "Show average income by gender as a bar chart"',
            label_visibility="collapsed",
        )
    with btn_col:
        generate = st.button("✨ Generate", type="primary", use_container_width=True)

    # ── Results ──────────────────────────────
    if generate:
        if not user_query.strip():
            st.warning("⚠️ Please enter a query first.")
        else:
            with st.spinner("Gemini is interpreting your query…"):
                try:
                    spec = query_gemini(user_query, df.columns.tolist())
                except json.JSONDecodeError as e:
                    st.error(f"❌ Gemini returned invalid JSON — {e}")
                    st.stop()
                except Exception as e:
                    st.error(f"❌ Gemini API error — {e}")
                    st.stop()

            st.success("✅ Query interpreted successfully!")

            with st.expander("🔍 Gemini's JSON interpretation", expanded=False):
                st.json(spec)

            try:
                result_df = process_data(df, spec)
            except ValueError as e:
                st.error(f"❌ Data processing error — {e}")
                st.stop()

            # Chart card — header in HTML, widget after closing tag
            st.markdown('<div class="card"><div class="card-title">📈 Generated Chart</div></div>', unsafe_allow_html=True)
            render_chart(result_df, spec)

            # Data card — header in HTML, widget after closing tag
            st.markdown(
                f'<div class="card"><div class="card-title">📊 Processed Data <span class="badge">{len(result_df)} rows</span></div></div>',
                unsafe_allow_html=True,
            )
            st.dataframe(result_df, use_container_width=True)