import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import re
import os

st.set_page_config(
    page_title="Marketing AI Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from constants import (
    BENCHMARK_THRESHOLDS,
    POWER_WORDS,
    CTA_KEYWORDS,
    URGENCY_WORDS,
    CLARITY_POSITIVE,
    TEMPLATE_AD_COPY,
)

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

def inject_css():
    st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 1.5rem !important; padding-bottom: 2rem !important;}

    /* App background */
    .stApp {background: #080D16;}

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B1220 0%, #080D16 100%) !important;
        border-right: 1px solid #162035 !important;
    }
    [data-testid="stSidebar"] .block-container {padding-top: 1rem !important;}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #0C1322;
        border: 1px solid #162035;
        border-radius: 14px;
        padding: 5px;
        gap: 2px;
        margin-bottom: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: #64748B;
        font-weight: 500;
        font-size: 0.9rem;
        padding: 10px 22px;
        transition: color 0.15s;
    }
    .stTabs [data-baseweb="tab"]:hover {color: #94A3B8;}
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4A90D9 0%, #5B3FE0 100%) !important;
        color: #fff !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 12px rgba(74,144,217,0.35);
    }
    .stTabs [data-baseweb="tab-highlight"] {display: none !important;}
    .stTabs [data-baseweb="tab-border"] {display: none !important;}

    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4A90D9 0%, #5B3FE0 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        transition: opacity 0.2s, box-shadow 0.2s !important;
        box-shadow: 0 2px 10px rgba(74,144,217,0.3) !important;
    }
    .stButton > button[kind="primary"]:hover {
        opacity: 0.88 !important;
        box-shadow: 0 4px 16px rgba(74,144,217,0.45) !important;
    }
    .stButton > button[kind="secondary"] {
        background: #0C1322 !important;
        border: 1px solid #1E2E45 !important;
        border-radius: 10px !important;
        color: #94A3B8 !important;
        font-weight: 500 !important;
    }

    /* Inputs */
    .stTextInput input, .stTextArea textarea {
        background: #0A1020 !important;
        border: 1px solid #1E2E45 !important;
        border-radius: 9px !important;
        color: #E2E8F0 !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #4A90D9 !important;
        box-shadow: 0 0 0 3px rgba(74,144,217,0.12) !important;
    }
    .stTextInput label, .stTextArea label {
        color: #94A3B8 !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.04em !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: #0A1020 !important;
        border: 1px solid #1E2E45 !important;
        border-radius: 9px !important;
    }
    .stSelectbox label {
        color: #94A3B8 !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.04em !important;
    }

    /* Radio */
    .stRadio label {color: #94A3B8 !important; font-size: 0.85rem !important;}

    /* Slider */
    .stSlider label {color: #94A3B8 !important; font-size: 0.82rem !important; font-weight: 600 !important;}
    .stSlider [data-testid="stThumbValue"] {color: #4A90D9 !important;}

    /* Expander */
    [data-testid="stExpander"] {
        background: #0A1020 !important;
        border: 1px solid #1E2E45 !important;
        border-radius: 12px !important;
        margin-bottom: 10px;
    }
    [data-testid="stExpander"] summary {
        color: #CBD5E1 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }

    /* Metric */
    [data-testid="stMetric"] {
        background: #0A1020;
        border: 1px solid #1E2E45;
        border-radius: 12px;
        padding: 16px 20px;
        transition: border-color 0.2s;
    }
    [data-testid="stMetric"]:hover {border-color: #4A90D9;}
    [data-testid="stMetricLabel"] p {
        color: #64748B !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    [data-testid="stMetricValue"] {color: #F1F5F9 !important; font-weight: 700 !important;}

    /* Data editor / dataframe */
    [data-testid="stDataFrameContainer"] {
        border: 1px solid #1E2E45 !important;
        border-radius: 12px !important;
        overflow: hidden;
    }

    /* File uploader */
    [data-testid="stFileUploaderDropzone"] {
        background: #0A1020 !important;
        border: 1px dashed #1E2E45 !important;
        border-radius: 12px !important;
    }

    /* Divider */
    hr {border-color: #1E2E45 !important; margin: 20px 0 !important;}

    /* Alert boxes */
    [data-testid="stAlert"] {border-radius: 10px !important;}

    /* ============================================================
       CUSTOM COMPONENT CLASSES
       ============================================================ */

    .app-banner {
        background: linear-gradient(135deg, #0C1829 0%, #101E3A 45%, #0B1220 100%);
        border: 1px solid #1E2E45;
        border-radius: 18px;
        padding: 30px 36px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .app-banner::before {
        content: '';
        position: absolute;
        top: -80px; right: -60px;
        width: 280px; height: 280px;
        background: radial-gradient(circle, rgba(74,144,217,0.14) 0%, transparent 65%);
        pointer-events: none;
    }
    .app-banner::after {
        content: '';
        position: absolute;
        bottom: -60px; left: 30%;
        width: 200px; height: 200px;
        background: radial-gradient(circle, rgba(91,63,224,0.08) 0%, transparent 65%);
        pointer-events: none;
    }
    .banner-title {
        font-size: 1.9rem;
        font-weight: 800;
        color: #F1F5F9;
        margin: 0 0 6px 0;
        letter-spacing: -0.02em;
    }
    .banner-sub {
        color: #64748B;
        font-size: 0.92rem;
        margin: 0 0 18px 0;
    }
    .banner-pills {display: flex; gap: 10px; flex-wrap: wrap;}
    .banner-pill {
        background: rgba(255,255,255,0.05);
        border: 1px solid #1E2E45;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.75rem;
        color: #94A3B8;
        font-weight: 500;
    }

    /* KPI card (Tab 2) */
    .kpi-card {
        background: linear-gradient(145deg, #0C1322, #0A1020);
        border: 1px solid #1E2E45;
        border-radius: 14px;
        padding: 18px 20px;
        transition: border-color 0.2s, transform 0.2s;
    }
    .kpi-card:hover {border-color: #4A90D9; transform: translateY(-2px);}
    .kpi-label {color:#64748B;font-size:0.70rem;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;margin-bottom:8px;}
    .kpi-value {color:#F1F5F9;font-size:1.7rem;font-weight:700;line-height:1;margin-bottom:5px;}
    .kpi-bench {color:#64748B;font-size:0.74rem;}
    .kpi-good .kpi-value {color:#27AE60;}
    .kpi-warn .kpi-value {color:#F39C12;}
    .kpi-bad  .kpi-value {color:#E74C3C;}

    /* Variant card (Tab 1) */
    .variant-wrap {
        background: linear-gradient(145deg, #0C1322, #0A1020);
        border-radius: 14px;
        padding: 22px 24px;
        margin-bottom: 18px;
        border-top: 1px solid #1E2E45;
        border-right: 1px solid #1E2E45;
        border-bottom: 1px solid #1E2E45;
        border-left: 4px solid;
        transition: border-top-color 0.2s;
    }
    .variant-header {display:flex;align-items:center;gap:12px;margin-bottom:16px;}
    .variant-badge {
        display:inline-flex;align-items:center;
        padding:4px 14px;border-radius:20px;
        font-size:0.75rem;font-weight:700;letter-spacing:0.07em;
    }
    .field-label {color:#64748B;font-size:0.70rem;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;margin-bottom:6px;}
    .copy-box {
        background:#060B14;border:1px solid #1E2E45;border-radius:8px;
        padding:10px 14px;font-family:monospace;font-size:0.88rem;
        color:#E2E8F0;min-height:36px;word-break:break-word;line-height:1.5;
    }
    .char-badge {display:inline-block;padding:2px 8px;border-radius:10px;font-size:0.70rem;font-weight:700;margin-left:6px;}
    .char-ok {background:rgba(39,174,96,0.15);color:#27AE60;}
    .char-bad {background:rgba(231,76,60,0.15);color:#E74C3C;}
    .rationale-box {
        background:rgba(74,144,217,0.06);border:1px solid rgba(74,144,217,0.15);
        border-radius:8px;padding:10px 14px;margin-top:14px;
        font-size:0.85rem;color:#94A3B8;
    }

    /* Section label */
    .sec-label {
        display:flex;align-items:center;gap:8px;
        color:#94A3B8;font-size:0.70rem;font-weight:700;
        text-transform:uppercase;letter-spacing:0.1em;
        margin:26px 0 12px;
    }
    .sec-label::before {
        content:'';display:block;width:3px;height:14px;
        background:linear-gradient(180deg,#4A90D9,#5B3FE0);border-radius:2px;flex-shrink:0;
    }

    /* Analysis card */
    .analysis-card {
        background:linear-gradient(135deg,#0B1829 0%,#0A1020 100%);
        border:1px solid #1E2E45;border-radius:14px;padding:24px;margin-top:16px;
    }
    .analysis-card p, .analysis-card li {color:#CBD5E1;font-size:0.9rem;line-height:1.7;}
    .analysis-card strong {color:#F1F5F9;}

    /* Winner card */
    .winner-card {
        background:linear-gradient(135deg,rgba(74,144,217,0.09) 0%,rgba(91,63,224,0.09) 100%);
        border:1px solid rgba(74,144,217,0.30);border-radius:14px;padding:20px 24px;
    }
    .winner-title {color:#4A90D9;font-weight:700;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;}
    .winner-text {color:#E2E8F0;font-size:0.92rem;line-height:1.6;}

    /* Scoring criteria grid */
    .criteria-grid {display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px;}
    .criteria-item {
        background:#0A1020;border:1px solid #1E2E45;border-radius:10px;
        padding:14px;text-align:center;
    }
    .criteria-icon {font-size:1.4rem;margin-bottom:6px;}
    .criteria-name {color:#F1F5F9;font-weight:700;font-size:0.85rem;margin-bottom:4px;}
    .criteria-weight {color:#64748B;font-size:0.75rem;}

    /* Sidebar content */
    .sidebar-logo {
        display:flex;align-items:center;gap:10px;
        padding:16px 0 20px;border-bottom:1px solid #162035;margin-bottom:16px;
    }
    .sidebar-icon {font-size:1.8rem;}
    .sidebar-name {color:#F1F5F9;font-weight:700;font-size:0.95rem;line-height:1.2;}
    .sidebar-tagline {color:#64748B;font-size:0.75rem;}

    .api-ok {
        display:flex;align-items:center;gap:8px;
        background:rgba(39,174,96,0.10);border:1px solid rgba(39,174,96,0.25);
        border-radius:9px;padding:10px 14px;color:#27AE60;font-weight:600;font-size:0.83rem;
    }
    .api-warn {
        display:flex;align-items:center;gap:8px;
        background:rgba(243,156,18,0.10);border:1px solid rgba(243,156,18,0.25);
        border-radius:9px;padding:10px 14px;color:#F39C12;font-weight:600;font-size:0.83rem;
    }
    .dot {width:8px;height:8px;border-radius:50%;display:inline-block;flex-shrink:0;}
    .dot-g {background:#27AE60;box-shadow:0 0 6px #27AE6066;}
    .dot-a {background:#F39C12;box-shadow:0 0 6px #F39C1266;}

    .sidebar-stat {
        display:flex;justify-content:space-between;align-items:center;
        padding:8px 0;border-bottom:1px solid #162035;
    }
    .stat-label {color:#64748B;font-size:0.78rem;}
    .stat-val {color:#CBD5E1;font-size:0.78rem;font-weight:600;}

    .sidebar-footer {
        position:absolute;bottom:1.5rem;left:1rem;right:1rem;
        border-top:1px solid #162035;padding-top:14px;
    }
    .footer-author {color:#94A3B8;font-size:0.78rem;font-weight:600;}
    .footer-note {color:#475569;font-size:0.72rem;margin-top:4px;line-height:1.5;}

    /* Legend pills */
    .legend-pill {
        display:inline-flex;align-items:center;gap:5px;
        padding:4px 12px;border-radius:20px;font-size:0.76rem;font-weight:600;
        margin-right:6px;
    }
    .lp-green {background:rgba(39,174,96,0.15);border:1px solid rgba(39,174,96,0.3);color:#27AE60;}
    .lp-amber {background:rgba(243,156,18,0.15);border:1px solid rgba(243,156,18,0.3);color:#F39C12;}
    .lp-red   {background:rgba(231,76,60,0.15);border:1px solid rgba(231,76,60,0.3);color:#E74C3C;}

    /* Tab 1 form card */
    .form-card {
        background:#0A1020;border:1px solid #1E2E45;border-radius:14px;padding:24px;margin-bottom:20px;
    }
    </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def get_anthropic_client():
    try:
        import anthropic
        api_key = None
        try:
            api_key = st.secrets.get("ANTHROPIC_API_KEY")
        except Exception:
            pass
        if not api_key:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
        if api_key:
            return anthropic.Anthropic(api_key=api_key)
    except ImportError:
        pass
    return None


OBJECTIVE_COLORS = {
    "Awareness": "#4A90D9",
    "Traffic": "#27AE60",
    "Conversions": "#F39C12",
    "Leads": "#9B59B6",
}

GREEN = "#27AE60"
AMBER = "#F39C12"
RED   = "#E74C3C"


# ---------------------------------------------------------------------------
# TAB 1 - Ad Copy Generator
# ---------------------------------------------------------------------------

def _call_ai_for_ad_copy(client, product, audience, objective, tone, usp):
    prompt = (
        f"You are an expert digital marketing copywriter. Generate 3 distinct ad copy variants.\n\n"
        f"Product/Service: {product}\n"
        f"Target Audience: {audience}\n"
        f"Campaign Objective: {objective}\n"
        f"Tone: {tone}\n"
        f"Key Selling Point: {usp}\n\n"
        f"For each variant provide:\n"
        f"1. headline - max 40 characters, no em dashes\n"
        f"2. primary_text - max 125 characters, no em dashes\n"
        f"3. cta - 2 to 4 words\n"
        f"4. rationale - one sentence explaining why this suits a {objective} objective\n\n"
        f"Return ONLY a valid JSON array of 3 objects with keys: headline, primary_text, cta, rationale.\n"
        f"Each variant must take a meaningfully different creative angle."
    )
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    text = msg.content[0].text
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        return json.loads(match.group())[:3]
    return None


def _template_ad_copy(product, audience, objective, tone, usp):
    tone_words = {
        "Professional": ["industry-leading", "enterprise-grade", "proven"],
        "Casual": ["super easy", "you will love", "pretty amazing"],
        "Urgent": ["today only", "right now", "before it is gone"],
        "Inspirational": ["transform", "elevate", "unlock your potential with"],
    }
    modifiers = tone_words.get(tone, ["trusted", "powerful", "effective"])
    templates = TEMPLATE_AD_COPY[objective]
    variants = []
    for i, tmpl in enumerate(templates[:3]):
        mod = modifiers[i % len(modifiers)]
        headline = tmpl["headline"].format(product=product[:18], modifier=mod, usp=usp[:20])[:40]
        primary_text = tmpl["primary_text"].format(product=product, audience=audience, usp=usp, modifier=mod)[:125]
        variants.append({
            "headline": headline,
            "primary_text": primary_text,
            "cta": tmpl["cta"],
            "rationale": tmpl["rationale"].format(objective=objective, tone=tone),
        })
    return variants


def render_ad_copy_tab():
    st.markdown('<div class="sec-label">Campaign Configuration</div>', unsafe_allow_html=True)

    with st.container():
        col_l, col_r = st.columns([3, 2], gap="large")
        with col_l:
            product  = st.text_input("Product / Service Name", placeholder="e.g., CloudSync Pro")
            audience = st.text_input("Target Audience", placeholder="e.g., Small business owners aged 25 to 45")
            usp      = st.text_input("Key Selling Point", placeholder="e.g., Saves 5 hours per week")
        with col_r:
            objective = st.selectbox("Campaign Objective", ["Awareness", "Traffic", "Conversions", "Leads"])
            tone      = st.selectbox("Tone", ["Professional", "Casual", "Urgent", "Inspirational"])
            obj_color = OBJECTIVE_COLORS.get(objective, "#4A90D9")
            st.markdown(
                f"<div style='margin-top:14px;padding:12px 16px;background:rgba(74,144,217,0.07);"
                f"border:1px solid #1E2E45;border-radius:10px;'>"
                f"<div style='color:#64748B;font-size:0.70rem;font-weight:700;text-transform:uppercase;"
                f"letter-spacing:0.08em;margin-bottom:6px;'>Objective Preview</div>"
                f"<div style='display:flex;align-items:center;gap:8px;'>"
                f"<span style='width:10px;height:10px;border-radius:50%;background:{obj_color};display:inline-block;flex-shrink:0'></span>"
                f"<span style='color:#CBD5E1;font-weight:600;font-size:0.88rem;'>{objective}</span>"
                f"<span style='color:#64748B;font-size:0.80rem;'>| {tone} tone</span>"
                f"</div></div>",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Generate Ad Copy", type="primary", use_container_width=True):
        if not product or not audience or not usp:
            st.error("Please fill in Product Name, Target Audience, and Key Selling Point.")
            return

        with st.spinner("Crafting your ad variants..."):
            client = get_anthropic_client()
            variants, used_ai = None, False
            if client:
                try:
                    variants = _call_ai_for_ad_copy(client, product, audience, objective, tone, usp)
                    used_ai = True
                except Exception as exc:
                    st.warning(f"AI generation unavailable ({str(exc)[:60]}). Using template engine.")
            if not variants:
                variants = _template_ad_copy(product, audience, objective, tone, usp)

        st.markdown('<div class="sec-label">Generated Variants</div>', unsafe_allow_html=True)

        source_badge = (
            '<span style="background:rgba(39,174,96,0.15);border:1px solid rgba(39,174,96,0.3);'
            'color:#27AE60;padding:3px 10px;border-radius:20px;font-size:0.73rem;font-weight:700;">'
            'AI Generated</span>'
            if used_ai else
            '<span style="background:rgba(74,144,217,0.15);border:1px solid rgba(74,144,217,0.3);'
            'color:#4A90D9;padding:3px 10px;border-radius:20px;font-size:0.73rem;font-weight:700;">'
            'Template Engine</span>'
        )
        st.markdown(f"<div style='margin-bottom:16px;'>{source_badge}</div>", unsafe_allow_html=True)

        color = OBJECTIVE_COLORS.get(objective, "#4A90D9")
        labels = ["A", "B", "C"]

        for i, v in enumerate(variants):
            hl   = v.get("headline", "")
            pt   = v.get("primary_text", "")
            cta  = v.get("cta", "Learn More")
            rat  = v.get("rationale", "")
            hlen = len(hl)
            ptlen = len(pt)
            hbadge = f'<span class="char-badge char-ok">{hlen}/40</span>' if hlen <= 40 else f'<span class="char-badge char-bad">{hlen}/40</span>'
            ptbadge = f'<span class="char-badge char-ok">{ptlen}/125</span>' if ptlen <= 125 else f'<span class="char-badge char-bad">{ptlen}/125</span>'

            st.markdown(
                f'<div class="variant-wrap" style="border-left-color:{color};">'
                f'<div class="variant-header">'
                f'<span class="variant-badge" style="background:rgba(74,144,217,0.12);'
                f'border:1px solid rgba(74,144,217,0.25);color:#94A3B8;">VARIANT {labels[i]}</span>'
                f'<span style="background:{color}22;border:1px solid {color}44;color:{color};'
                f'padding:3px 10px;border-radius:20px;font-size:0.73rem;font-weight:700;">{objective}</span>'
                f'</div>'
                f'<div style="display:grid;grid-template-columns:1fr 1fr auto;gap:16px;align-items:start;">'

                f'<div><div class="field-label">Headline {hbadge}</div>'
                f'<div class="copy-box">{hl}</div></div>'

                f'<div><div class="field-label">Primary Text {ptbadge}</div>'
                f'<div class="copy-box">{pt}</div></div>'

                f'<div><div class="field-label">CTA Button</div>'
                f'<div style="background:{color};color:#fff;padding:10px 16px;border-radius:8px;'
                f'text-align:center;font-weight:700;font-size:0.85rem;white-space:nowrap;'
                f'margin-top:0;min-width:110px;">{cta}</div></div>'

                f'</div>'
                f'<div class="rationale-box">'
                f'<strong style="color:#CBD5E1;">Why this works for {objective}:</strong> {rat}'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------------------------
# TAB 2 - Campaign Performance Analyzer
# ---------------------------------------------------------------------------

def _metric_color(col_name, value):
    cfg = BENCHMARK_THRESHOLDS.get(col_name)
    if not cfg:
        return ""
    good, warn, higher = cfg["good"], cfg["warn"], cfg["higher_is_better"]
    bg = (GREEN if (value >= good if higher else value <= good)
          else AMBER if (value >= warn if higher else value <= warn)
          else RED)
    return f"background-color:{bg};color:#fff;font-weight:600"


def _style_row(row):
    styles = []
    for col in row.index:
        if col in BENCHMARK_THRESHOLDS:
            try:
                val = float(str(row[col]).replace("%","").replace("$","").replace(",","").strip())
                styles.append(_metric_color(col, val))
            except (ValueError, TypeError):
                styles.append("")
        else:
            styles.append("")
    return styles


def _analyze_with_ai(client, df_str):
    prompt = (
        "You are a senior digital marketing analyst. Analyze this campaign data:\n\n"
        f"{df_str}\n\n"
        "Benchmarks: CTR > 1% good, ROAS > 2x profitable, CPC < $2 efficient, CPM < $5 efficient.\n\n"
        "Provide three sections:\n"
        "**What is Working Well** (2 to 3 bullet points with specific numbers)\n"
        "**What is Underperforming** (2 to 3 bullet points with specific numbers)\n"
        "**Three Actionable Recommendations** (numbered, each with an expected impact)\n\n"
        "Be concrete. Reference campaign names and exact metrics. No em dashes."
    )
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=900,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def _analyze_with_rules(df):
    good_pts, bad_pts, recs = [], [], []
    for _, row in df.iterrows():
        name = row.get("Campaign", "This campaign")
        for col, higher, thr_good, thr_warn, unit in [
            ("CTR (%)", True, 1.5, 0.8, "%"),
            ("ROAS", True, 3.0, 1.5, "x"),
            ("CPC ($)", False, 1.5, 2.5, ""),
            ("CPM ($)", False, 4.0, 8.0, ""),
        ]:
            if col not in df.columns:
                continue
            try:
                val = float(str(row[col]).replace("$","").replace("%","").replace("x","").replace(",",""))
            except (ValueError, TypeError):
                continue
            if higher:
                if val >= thr_good:
                    good_pts.append(f"{name} achieves strong {col} of {val:.2f}{unit} (benchmark: above {thr_good}{unit})")
                elif val < thr_warn:
                    bad_pts.append(f"{name} {col} of {val:.2f}{unit} is below the {thr_warn}{unit} threshold")
                    if col == "CTR (%)":
                        recs.append(f"Refresh creatives for {name} to lift CTR above 1%")
                    elif col == "ROAS":
                        recs.append(f"Tighten audience and bid strategy for {name} to reach 2x ROAS")
            else:
                if val <= thr_good:
                    good_pts.append(f"{name} keeps {col} efficient at {val:.2f} (target: below {thr_good})")
                elif val > thr_warn:
                    bad_pts.append(f"{name} {col} of {val:.2f} exceeds the {thr_warn} target")
                    if col == "CPC ($)":
                        recs.append(f"Narrow audience targeting for {name} to bring CPC toward $1.50")

    if not good_pts:
        good_pts = [
            "All campaigns are generating measurable impressions and driving site traffic",
            "Spend is diversified across multiple campaigns, reducing single-channel risk",
        ]
    if not bad_pts:
        bad_pts = [
            "Minor efficiency gaps across campaigns that bid optimization can address",
            "Room to improve conversion volume with audience refinement",
        ]
    recs = (recs + [
        "A/B test ad headlines across all campaigns to target a 15 to 20% CTR improvement",
        "Apply dayparting to concentrate budget on peak conversion hours",
        "Build lookalike audiences from your top 10% converters to lift ROAS",
    ])[:3]

    out = ["**What is Working Well**"] + [f"- {p}" for p in good_pts[:3]]
    out += ["", "**What is Underperforming**"] + [f"- {p}" for p in bad_pts[:3]]
    out += ["", "**Three Actionable Recommendations**"] + [f"{i}. {r}" for i, r in enumerate(recs, 1)]
    return "\n".join(out)


DEFAULT_CAMPAIGN_DATA = {
    "Campaign": ["Brand Awareness Q4", "Lead Gen - Email List", "Retargeting - Abandoned Cart"],
    "Impressions": [450000, 120000, 85000],
    "Clicks": [3150, 2040, 2125],
    "Conversions": [63, 204, 468],
    "Spend ($)": [1800, 1560, 1275],
    "Reach": [380000, 95000, 72000],
    "CTR (%)": [0.70, 1.70, 2.50],
    "CPC ($)": [0.57, 0.76, 0.60],
    "CPM ($)": [4.00, 13.00, 15.00],
    "ROAS": [1.75, 3.20, 5.50],
}


def _kpi_status(val, col_name):
    cfg = BENCHMARK_THRESHOLDS.get(col_name, {})
    if not cfg:
        return "kpi-card"
    good, warn, higher = cfg["good"], cfg["warn"], cfg["higher_is_better"]
    ok  = val >= good if higher else val <= good
    mid = val >= warn if higher else val <= warn
    return "kpi-card kpi-good" if ok else ("kpi-card kpi-warn" if mid else "kpi-card kpi-bad")


def render_performance_tab():
    st.markdown('<div class="sec-label">Industry Benchmarks</div>', unsafe_allow_html=True)

    b1, b2, b3, b4 = st.columns(4, gap="medium")
    benchmarks = [
        (b1, "Click-Through Rate", "> 1.0%", "CTR (%)"),
        (b2, "Return on Ad Spend", "> 2.0x", "ROAS"),
        (b3, "Cost per Click", "< $2.00", "CPC ($)"),
        (b4, "Cost per Thousand", "< $5.00", "CPM ($)"),
    ]
    for col, label, target, _ in benchmarks:
        col.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value" style="font-size:1.4rem;color:#4A90D9;">{target}</div>'
            f'<div class="kpi-bench">Industry benchmark</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="sec-label">Campaign Data</div>', unsafe_allow_html=True)

    method = st.radio("Input method", ["Manual Entry", "Upload CSV"], horizontal=True, label_visibility="collapsed")
    df = None

    if method == "Manual Entry":
        df = st.data_editor(
            pd.DataFrame(DEFAULT_CAMPAIGN_DATA),
            use_container_width=True,
            num_rows="dynamic",
            key="campaign_editor",
        )
    else:
        uploaded = st.file_uploader("Upload CSV file", type=["csv"])
        if uploaded:
            df = pd.read_csv(uploaded)
            st.dataframe(df, use_container_width=True)
        else:
            st.markdown(
                '<div style="background:#0A1020;border:1px solid #1E2E45;border-radius:10px;'
                'padding:16px;color:#64748B;font-size:0.85rem;">Expected columns: Campaign, '
                'Impressions, Clicks, Conversions, Spend ($), Reach, CTR (%), CPC ($), CPM ($), ROAS</div>',
                unsafe_allow_html=True,
            )

    if df is not None and not df.empty:
        st.markdown('<div class="sec-label">Performance Overview</div>', unsafe_allow_html=True)

        st.markdown(
            '<div style="margin-bottom:12px;">'
            '<span class="legend-pill lp-green"><span style="width:7px;height:7px;border-radius:50%;'
            'background:#27AE60;display:inline-block;"></span> Strong</span>'
            '<span class="legend-pill lp-amber"><span style="width:7px;height:7px;border-radius:50%;'
            'background:#F39C12;display:inline-block;"></span> Needs Attention</span>'
            '<span class="legend-pill lp-red"><span style="width:7px;height:7px;border-radius:50%;'
            'background:#E74C3C;display:inline-block;"></span> Underperforming</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        try:
            styled = df.style.apply(_style_row, axis=1)
            st.dataframe(styled, use_container_width=True)
        except Exception:
            st.dataframe(df, use_container_width=True)

        # Aggregate KPI row
        st.markdown('<div class="sec-label">Aggregate KPIs</div>', unsafe_allow_html=True)
        kpi_defs = [
            ("Avg CTR", "CTR (%)", lambda v: f"{v:.2f}%"),
            ("Avg CPC", "CPC ($)", lambda v: f"${v:.2f}"),
            ("Avg CPM", "CPM ($)", lambda v: f"${v:.2f}"),
            ("Avg ROAS", "ROAS", lambda v: f"{v:.2f}x"),
            ("Total Conv.", "Conversions", lambda v: f"{v:,.0f}"),
        ]
        agg_cols = st.columns(5, gap="medium")
        computed = {}
        for col_w, (label, col_name, fmt_fn) in zip(agg_cols, kpi_defs):
            if col_name not in df.columns:
                continue
            try:
                nums = pd.to_numeric(
                    df[col_name].astype(str).str.replace(r"[$%x,]", "", regex=True),
                    errors="coerce",
                )
                val = nums.sum() if "Conv" in label else nums.mean()
                computed[col_name] = val
                css = _kpi_status(val, col_name)
                col_w.markdown(
                    f'<div class="{css}">'
                    f'<div class="kpi-label">{label}</div>'
                    f'<div class="kpi-value">{fmt_fn(val)}</div>'
                    f'<div class="kpi-bench">across {len(df)} campaigns</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            except Exception:
                pass

        # Campaign ROAS comparison chart
        if "ROAS" in df.columns and "Campaign" in df.columns:
            st.markdown('<div class="sec-label">Campaign ROAS vs Benchmark</div>', unsafe_allow_html=True)
            try:
                roas_vals = pd.to_numeric(
                    df["ROAS"].astype(str).str.replace(r"[x,]", "", regex=True), errors="coerce"
                )
                campaigns = df["Campaign"].tolist()
                bar_colors = [GREEN if v >= 2 else (AMBER if v >= 1.5 else RED) for v in roas_vals]

                fig_roas = go.Figure()
                fig_roas.add_trace(go.Bar(
                    x=roas_vals.tolist(),
                    y=campaigns,
                    orientation="h",
                    marker_color=bar_colors,
                    text=[f"{v:.2f}x" for v in roas_vals],
                    textposition="outside",
                    textfont=dict(color="#CBD5E1", size=13),
                    hovertemplate="%{y}: %{x:.2f}x ROAS<extra></extra>",
                ))
                fig_roas.add_vline(
                    x=2.0, line_dash="dash", line_color=AMBER, line_width=1.5,
                    annotation_text="2x benchmark", annotation_font_color=AMBER,
                    annotation_position="top right",
                )
                fig_roas.update_layout(
                    height=220 + len(campaigns) * 30,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(title="ROAS", color="#64748B", gridcolor="#162035", range=[0, max(roas_vals.max() * 1.25, 3)]),
                    yaxis=dict(color="#CBD5E1", automargin=True),
                    margin=dict(l=0, r=60, t=10, b=30),
                    font=dict(color="#94A3B8", size=12),
                    showlegend=False,
                )
                st.plotly_chart(fig_roas, use_container_width=True)
            except Exception:
                pass

        # AI Analysis
        st.markdown('<div class="sec-label">AI Performance Analysis</div>', unsafe_allow_html=True)
        if st.button("Analyze Campaign Performance", type="primary"):
            with st.spinner("Analyzing your campaigns..."):
                client = get_anthropic_client()
                df_str = df.to_string(index=False)
                if client:
                    try:
                        analysis = _analyze_with_ai(client, df_str)
                        source = "Powered by Anthropic claude-haiku-4-5"
                        src_color = "#27AE60"
                    except Exception as exc:
                        st.warning(f"AI unavailable ({str(exc)[:60]}). Using rule-based engine.")
                        analysis = _analyze_with_rules(df)
                        source = "Rule-based analysis"
                        src_color = "#4A90D9"
                else:
                    analysis = _analyze_with_rules(df)
                    source = "Rule-based analysis (add ANTHROPIC_API_KEY to enable AI)"
                    src_color = "#4A90D9"

            st.markdown(
                f'<div style="margin-bottom:8px;">'
                f'<span style="background:rgba(74,144,217,0.12);border:1px solid rgba(74,144,217,0.25);'
                f'color:{src_color};padding:4px 12px;border-radius:20px;font-size:0.73rem;font-weight:700;">'
                f'{source}</span></div>',
                unsafe_allow_html=True,
            )
            st.markdown(f'<div class="analysis-card">', unsafe_allow_html=True)
            st.markdown(analysis)
            st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# TAB 3 - A/B Variant Scorer
# ---------------------------------------------------------------------------

def _score_clarity(headline, body):
    score = 5.0
    words_h = len(headline.split())
    score += 2.0 if 4 <= words_h <= 8 else (-1.0 if words_h < 3 or words_h > 12 else 0)
    words_b = len(body.split())
    score += 2.0 if 15 <= words_b <= 35 else (-2.0 if words_b < 5 else (-1.0 if words_b > 55 else 0))
    score += min(sum(1 for w in CLARITY_POSITIVE if w in body.lower()) * 0.5, 1.5)
    if "?" in headline:
        score -= 0.5
    return min(max(round(score, 1), 0.0), 10.0)


def _score_urgency(headline, body):
    score = 3.0
    combined = (headline + " " + body).lower()
    score += min(sum(1 for w in URGENCY_WORDS if w in combined) * 1.2, 5.0)
    score += min(combined.count("!") * 0.5, 1.5)
    if re.search(r"\d+", combined):
        score += 0.5
    return min(max(round(score, 1), 0.0), 10.0)


def _score_relevance(headline, body):
    score = 4.0
    combined = (headline + " " + body).lower()
    score += min(sum(1 for w in POWER_WORDS if w in combined) * 0.6, 3.0)
    if re.search(r"\d+%|\d+x|\$\d+|\d+ hours|\d+ days|\d+ minutes", combined):
        score += 1.5
    benefit_words = ["save", "get", "increase", "reduce", "improve", "boost", "gain", "earn"]
    score += min(sum(1 for w in benefit_words if w in combined) * 0.5, 1.5)
    return min(max(round(score, 1), 0.0), 10.0)


def _score_cta(headline, body):
    score = 3.0
    combined = (headline + " " + body).lower()
    score += min(sum(1 for kw in CTA_KEYWORDS if kw in combined) * 1.5, 5.0)
    action_verbs = ["start", "join", "discover", "unlock", "claim", "try", "get", "book", "download"]
    score += min(sum(1 for w in action_verbs if w in combined) * 0.5, 1.5)
    if "you" in combined or "your" in combined:
        score += 0.5
    return min(max(round(score, 1), 0.0), 10.0)


def _overall(clarity, urgency, relevance, cta):
    return round(clarity * 0.30 + urgency * 0.20 + relevance * 0.30 + cta * 0.20, 1)


RADAR_COLORS = [
    ("#4A90D9", "rgba(74,144,217,0.18)"),
    ("#E74C3C", "rgba(231,76,60,0.18)"),
    ("#27AE60", "rgba(39,174,96,0.18)"),
    ("#9B59B6", "rgba(155,89,182,0.18)"),
    ("#F39C12", "rgba(243,156,18,0.18)"),
]


def _make_radar(results_df):
    dims = ["Clarity", "Urgency", "Relevance", "CTA Strength"]
    fig = go.Figure()
    for i, (_, row) in enumerate(results_df.iterrows()):
        line_c, fill_c = RADAR_COLORS[i % len(RADAR_COLORS)]
        vals = [row[d] for d in dims] + [row[dims[0]]]
        fig.add_trace(go.Scatterpolar(
            r=vals,
            theta=dims + [dims[0]],
            fill="toself",
            name=row["Variant"],
            line=dict(color=line_c, width=2),
            fillcolor=fill_c,
        ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 10], color="#475569", gridcolor="#1E2E45", tickfont=dict(size=9)),
            angularaxis=dict(color="#94A3B8", gridcolor="#1E2E45"),
        ),
        showlegend=True,
        legend=dict(font=dict(color="#94A3B8", size=11), bgcolor="rgba(0,0,0,0)"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8"),
        height=360,
        margin=dict(l=40, r=40, t=30, b=30),
        title=dict(text="Radar Comparison", font=dict(size=13, color="#94A3B8"), x=0.5),
    )
    return fig


def _make_bar_chart(results_df):
    dim_colors = {
        "Clarity": "#4A90D9", "Urgency": "#E74C3C",
        "Relevance": "#27AE60", "CTA Strength": "#9B59B6", "Overall Score": "#F39C12",
    }
    fig = go.Figure()
    for dim in ["Clarity", "Urgency", "Relevance", "CTA Strength", "Overall Score"]:
        fig.add_trace(go.Bar(
            name=dim,
            x=results_df["Variant"].tolist(),
            y=results_df[dim].tolist(),
            marker_color=dim_colors[dim],
            text=[f"{v:.1f}" for v in results_df[dim].tolist()],
            textposition="outside",
            textfont=dict(size=11),
        ))
    fig.update_layout(
        barmode="group",
        xaxis=dict(color="#94A3B8", gridcolor="#1A2332"),
        yaxis=dict(range=[0, 12], color="#94A3B8", gridcolor="#1A2332", title="Score (0 to 10)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=1,
                    font=dict(size=11, color="#94A3B8"), bgcolor="rgba(0,0,0,0)"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8"),
        height=360,
        margin=dict(l=0, r=0, t=40, b=0),
        title=dict(text="Score by Dimension", font=dict(size=13, color="#94A3B8"), x=0.5),
    )
    return fig


def render_ab_scorer_tab():
    st.markdown(
        '<div class="criteria-grid">'
        '<div class="criteria-item"><div class="criteria-icon">💡</div>'
        '<div class="criteria-name">Clarity</div><div class="criteria-weight">30% weight</div></div>'
        '<div class="criteria-item"><div class="criteria-icon">📣</div>'
        '<div class="criteria-name">Relevance</div><div class="criteria-weight">30% weight</div></div>'
        '<div class="criteria-item"><div class="criteria-icon">⏰</div>'
        '<div class="criteria-name">Urgency</div><div class="criteria-weight">20% weight</div></div>'
        '<div class="criteria-item"><div class="criteria-icon">🎯</div>'
        '<div class="criteria-name">CTA Strength</div><div class="criteria-weight">20% weight</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sec-label">Variant Inputs</div>', unsafe_allow_html=True)
    num_variants = st.slider("Number of variants to score", min_value=2, max_value=5, value=2, label_visibility="collapsed")
    variants_input = []

    for i in range(num_variants):
        label = chr(65 + i)
        with st.expander(f"Variant {label}", expanded=(i < 2)):
            c1, c2 = st.columns(2, gap="medium")
            with c1:
                hl = st.text_input(f"Headline", key=f"ab_hl_{i}", placeholder="e.g., Save 3 Hours Daily with AI", label_visibility="collapsed")
                st.caption("Headline")
            with c2:
                bd = st.text_area(f"Ad Body", key=f"ab_bd_{i}", placeholder="e.g., Join 10,000 teams who automate their workflow. Start free today.", height=68, label_visibility="collapsed")
                st.caption("Ad Body")
        variants_input.append({"name": f"Variant {label}", "headline": hl, "body": bd})

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Score All Variants", type="primary", use_container_width=True):
        valid = [v for v in variants_input if v["headline"] and v["body"]]
        if len(valid) < 2:
            st.error("Please enter at least 2 complete variants (headline + body).")
            return

        rows = []
        for v in valid:
            cl = _score_clarity(v["headline"], v["body"])
            ur = _score_urgency(v["headline"], v["body"])
            rv = _score_relevance(v["headline"], v["body"])
            ct = _score_cta(v["headline"], v["body"])
            ov = _overall(cl, ur, rv, ct)
            rows.append({"Variant": v["name"], "Clarity": cl, "Urgency": ur,
                         "Relevance": rv, "CTA Strength": ct, "Overall Score": ov})

        results = pd.DataFrame(rows).sort_values("Overall Score", ascending=False).reset_index(drop=True)

        st.markdown('<div class="sec-label">Score Table</div>', unsafe_allow_html=True)

        def _cell_color(val):
            if not isinstance(val, (int, float)):
                return ""
            return (f"background-color:{GREEN};color:#fff" if val >= 7.0
                    else f"background-color:{AMBER};color:#fff" if val >= 5.0
                    else f"background-color:{RED};color:#fff")

        score_cols = ["Clarity", "Urgency", "Relevance", "CTA Strength", "Overall Score"]
        try:
            styled = results.style.map(_cell_color, subset=score_cols)
        except AttributeError:
            styled = results.style.applymap(_cell_color, subset=score_cols)
        st.dataframe(styled, use_container_width=True, hide_index=True)

        st.markdown('<div class="sec-label">Visual Comparison</div>', unsafe_allow_html=True)
        chart_col, radar_col = st.columns(2, gap="large")
        with chart_col:
            st.plotly_chart(_make_bar_chart(results), use_container_width=True)
        with radar_col:
            st.plotly_chart(_make_radar(results), use_container_width=True)

        # Winner card
        winner = results.iloc[0]
        runner = results.iloc[1] if len(results) > 1 else None
        best_dim = max(["Clarity", "Urgency", "Relevance", "CTA Strength"], key=lambda d: winner[d])
        rec = (
            f"<strong>{winner['Variant']}</strong> scores highest at <strong>{winner['Overall Score']:.1f}/10</strong>. "
            f"It leads on <strong>{best_dim}</strong> ({winner[best_dim]:.1f}/10)"
        )
        if runner is not None:
            gap = winner["Overall Score"] - runner["Overall Score"]
            rec += (
                f" and outscores {runner['Variant']} by {gap:.1f} points. Launch {winner['Variant']} first."
                if gap >= 0.5 else
                f". {runner['Variant']} ({runner['Overall Score']:.1f}/10) is close enough to run as a direct challenger."
            )
        st.markdown(
            f'<div class="winner-card">'
            f'<div class="winner-title">Recommendation</div>'
            f'<div class="winner-text">{rec}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Per-variant breakdown
        st.markdown('<div class="sec-label">Dimension Breakdown</div>', unsafe_allow_html=True)
        metric_cols = st.columns(len(valid), gap="medium")
        for col_w, (_, row) in zip(metric_cols, results.iterrows()):
            col_w.metric(f"{row['Variant']}", f"{row['Overall Score']}/10", label_visibility="visible")
            col_w.metric("Clarity", f"{row['Clarity']}/10")
            col_w.metric("Urgency", f"{row['Urgency']}/10")
            col_w.metric("Relevance", f"{row['Relevance']}/10")
            col_w.metric("CTA Strength", f"{row['CTA Strength']}/10")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    inject_css()

    # Sidebar
    with st.sidebar:
        client = get_anthropic_client()
        st.markdown(
            '<div class="sidebar-logo">'
            '<div class="sidebar-icon">📊</div>'
            '<div><div class="sidebar-name">Marketing AI</div>'
            '<div class="sidebar-tagline">Automation Platform</div></div>'
            '</div>',
            unsafe_allow_html=True,
        )

        if client:
            st.markdown(
                '<div class="api-ok"><span class="dot dot-g"></span>Anthropic API Connected</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="api-warn"><span class="dot dot-a"></span>API Not Configured</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div style='margin-top:8px;padding:10px;background:#0A1020;border:1px solid #1E2E45;"
                "border-radius:8px;color:#475569;font-size:0.75rem;line-height:1.6;'>"
                "Add <code style='background:#162035;padding:1px 5px;border-radius:4px;color:#94A3B8;"
                "font-size:0.78rem;'>ANTHROPIC_API_KEY</code> to your Streamlit secrets to enable AI. "
                "All tabs work in fallback mode without it.</div>",
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div style="color:#64748B;font-size:0.70rem;font-weight:700;text-transform:uppercase;'
            'letter-spacing:0.09em;margin-bottom:10px;">Platform Info</div>',
            unsafe_allow_html=True,
        )
        stats = [
            ("AI Model", "claude-haiku-4-5"),
            ("Framework", "Streamlit"),
            ("Charts", "Plotly"),
            ("Tabs", "3 tools"),
            ("Data", "Synthetic samples"),
        ]
        for label, val in stats:
            st.markdown(
                f'<div class="sidebar-stat">'
                f'<span class="stat-label">{label}</span>'
                f'<span class="stat-val">{val}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div style="border-top:1px solid #162035;padding-top:14px;">'
            '<div style="color:#94A3B8;font-size:0.78rem;font-weight:600;">Ridhan Parvendhan</div>'
            '<div style="color:#475569;font-size:0.72rem;margin-top:4px;line-height:1.6;">'
            'All sample data is synthetic and for demonstration purposes only.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    # App banner
    st.markdown(
        '<div class="app-banner">'
        '<div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:16px;">'
        '<div>'
        '<div class="banner-title">Marketing AI Platform</div>'
        '<div class="banner-sub">AI-powered tools for ad creation, campaign analysis, and variant scoring</div>'
        '<div class="banner-pills">'
        '<span class="banner-pill">Ad Copy Generator</span>'
        '<span class="banner-pill">Performance Analyzer</span>'
        '<span class="banner-pill">A/B Variant Scorer</span>'
        '</div>'
        '</div>'
        '<div style="text-align:right;">'
        '<div style="color:#64748B;font-size:0.72rem;font-weight:700;text-transform:uppercase;'
        'letter-spacing:0.09em;margin-bottom:6px;">Powered by</div>'
        '<div style="color:#4A90D9;font-size:0.85rem;font-weight:700;">Anthropic claude-haiku-4-5</div>'
        '<div style="color:#475569;font-size:0.75rem;margin-top:2px;">with rule-based fallback</div>'
        '</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs([
        "  Ad Copy Generator  ",
        "  Campaign Analyzer  ",
        "  A/B Variant Scorer  ",
    ])
    with tab1:
        render_ad_copy_tab()
    with tab2:
        render_performance_tab()
    with tab3:
        render_ab_scorer_tab()


if __name__ == "__main__":
    main()
