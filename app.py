import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import json
import re
import os

st.set_page_config(
    page_title="Marketing AI Platform",
    page_icon="🎯",
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

ACCENT = "#FF5E2C"
GREEN  = "#22C55E"
AMBER  = "#F59E0B"
RED    = "#EF4444"

OBJECTIVE_COLORS = {
    "Awareness":   "#6366F1",
    "Traffic":     "#10B981",
    "Conversions": "#FF5E2C",
    "Leads":       "#8B5CF6",
}


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

def inject_css():
    st.markdown(
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">',
        unsafe_allow_html=True,
    )

    css = (
        "*, *::before, *::after { font-family: 'Inter', -apple-system, sans-serif !important; }"
        "#MainMenu, footer, header { visibility: hidden; }"
        ".block-container { padding: 2.25rem 2.5rem !important; max-width: 1180px !important; }"
        ".stApp { background: #080808 !important; }"
        "[data-testid='stSidebar'] { background: #040404 !important; border-right: 1px solid rgba(255,255,255,0.05) !important; }"
        "[data-testid='stSidebar'] .block-container { padding: 1.5rem 1.25rem 1.5rem !important; }"
        ".stTabs [data-baseweb='tab-list'] { background: transparent !important; border: none !important; border-bottom: 1px solid rgba(255,255,255,0.07) !important; border-radius: 0 !important; padding: 0 !important; gap: 0 !important; margin-bottom: 32px !important; }"
        ".stTabs [data-baseweb='tab'] { background: transparent !important; border-radius: 0 !important; color: #484848 !important; font-weight: 400 !important; font-size: 0.875rem !important; padding: 12px 0 !important; margin-right: 28px !important; border-bottom: 2px solid transparent !important; margin-bottom: -1px !important; letter-spacing: 0.005em !important; transition: color 0.12s !important; }"
        ".stTabs [data-baseweb='tab']:hover { color: #999 !important; }"
        ".stTabs [aria-selected='true'] { background: transparent !important; color: #F0F0F0 !important; font-weight: 600 !important; border-bottom-color: #FF5E2C !important; }"
        ".stTabs [data-baseweb='tab-highlight'], .stTabs [data-baseweb='tab-border'] { display: none !important; }"
        ".stTextInput input, .stTextArea textarea { background: #0D0D0D !important; border: 1px solid rgba(255,255,255,0.07) !important; border-radius: 5px !important; color: #EBEBEB !important; font-size: 0.9rem !important; transition: border-color 0.12s !important; caret-color: #FF5E2C !important; }"
        ".stTextInput input:focus, .stTextArea textarea:focus { border-color: rgba(255,94,44,0.4) !important; box-shadow: 0 0 0 3px rgba(255,94,44,0.07) !important; }"
        ".stTextInput input::placeholder, .stTextArea textarea::placeholder { color: #2A2A2A !important; }"
        ".stTextInput label, .stTextArea label { color: #444 !important; font-size: 0.73rem !important; font-weight: 500 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; }"
        ".stSelectbox [data-baseweb='select'] > div:first-child { background: #0D0D0D !important; border: 1px solid rgba(255,255,255,0.07) !important; border-radius: 5px !important; transition: border-color 0.12s !important; }"
        ".stSelectbox [data-baseweb='select'] > div:first-child:hover { border-color: rgba(255,255,255,0.14) !important; }"
        ".stSelectbox label { color: #444 !important; font-size: 0.73rem !important; font-weight: 500 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; }"
        ".stButton > button { border-radius: 5px !important; font-weight: 500 !important; font-size: 0.875rem !important; letter-spacing: 0.01em !important; transition: background 0.12s !important; }"
        ".stButton > button[kind='primary'] { background: #FF5E2C !important; border: none !important; color: #fff !important; }"
        ".stButton > button[kind='primary']:hover { background: #E8501E !important; }"
        ".stButton > button[kind='secondary'] { background: transparent !important; border: 1px solid rgba(255,255,255,0.1) !important; color: #888 !important; }"
        ".stButton > button[kind='secondary']:hover { border-color: rgba(255,255,255,0.2) !important; color: #ccc !important; }"
        ".stRadio label span { color: #666 !important; font-size: 0.85rem !important; }"
        ".stSlider label { color: #444 !important; font-size: 0.73rem !important; font-weight: 500 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; }"
        ".stSlider [data-testid='stThumbValue'] { color: #FF5E2C !important; font-weight: 600 !important; }"
        "[data-testid='stExpander'] { border: 1px solid rgba(255,255,255,0.06) !important; border-radius: 5px !important; background: #0C0C0C !important; margin-bottom: 6px !important; }"
        "[data-testid='stExpander'] summary { color: #bbb !important; font-weight: 500 !important; font-size: 0.875rem !important; }"
        "[data-testid='stExpander'] summary:hover { color: #eee !important; }"
        "[data-testid='stMetric'] { background: transparent !important; border: none !important; padding: 0 !important; }"
        "[data-testid='stMetricLabel'] p { color: #383838 !important; font-size: 0.68rem !important; font-weight: 600 !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; }"
        "[data-testid='stMetricValue'] { color: #E8E8E8 !important; font-size: 1.45rem !important; font-weight: 700 !important; letter-spacing: -0.02em !important; font-variant-numeric: tabular-nums !important; }"
        "[data-testid='stDataFrameContainer'] { border: 1px solid rgba(255,255,255,0.06) !important; border-radius: 6px !important; overflow: hidden !important; }"
        "[data-testid='stFileUploaderDropzone'] { background: #0C0C0C !important; border: 1px dashed rgba(255,255,255,0.1) !important; border-radius: 6px !important; }"
        "[data-testid='stAlert'] { border-radius: 5px !important; }"
        "hr { border-color: rgba(255,255,255,0.06) !important; margin: 28px 0 !important; }"
        "::-webkit-scrollbar { width: 5px; height: 5px; }"
        "::-webkit-scrollbar-track { background: transparent; }"
        "::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.09); border-radius: 3px; }"
        "::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.16); }"
        ".sec { color: #333; font-size: 0.68rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; margin: 0 0 14px; display: block; }"
        ".analysis-text p, .analysis-text li { color: #888; font-size: 0.875rem; line-height: 1.75; }"
        ".analysis-text strong { color: #C8C8C8; }"
        ".analysis-text h2, .analysis-text h3 { color: #888; font-size: 0.875rem; font-weight: 600; margin-top: 20px; }"
    )

    components.html(
        f"""<script>
(function() {{
    var d = window.parent.document;
    var id = 'mktai-global-css';
    if (d.getElementById(id)) return;
    var s = d.createElement('style');
    s.id = id;
    s.textContent = {json.dumps(css)};
    d.head.appendChild(s);
}})();
</script>""",
        height=0,
        scrolling=False,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_anthropic_client():
    try:
        import anthropic
        key = None
        try:
            key = st.secrets.get("ANTHROPIC_API_KEY")
        except Exception:
            pass
        if not key:
            key = os.environ.get("ANTHROPIC_API_KEY")
        if key:
            return anthropic.Anthropic(api_key=key)
    except ImportError:
        pass
    return None


def _label(text):
    return f'<span class="sec">{text}</span>'


def _thin_rule():
    return '<div style="height:1px;background:rgba(255,255,255,0.06);margin:28px 0;"></div>'


# ---------------------------------------------------------------------------
# TAB 1 — Ad Copy Generator
# ---------------------------------------------------------------------------

def _call_ai_for_ad_copy(client, product, audience, objective, tone, usp):
    prompt = (
        f"You are an expert digital marketing copywriter. Generate 3 distinct ad copy variants.\n\n"
        f"Product/Service: {product}\n"
        f"Target Audience: {audience}\n"
        f"Campaign Objective: {objective}\n"
        f"Tone: {tone}\n"
        f"Key Selling Point: {usp}\n\n"
        f"Return ONLY a valid JSON array of 3 objects with keys: headline (max 40 chars), "
        f"primary_text (max 125 chars), cta (2-4 words), rationale (one sentence). "
        f"Each variant takes a meaningfully different creative angle. No em dashes."
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
    mods = {
        "Professional": ["industry-leading", "enterprise-grade", "proven"],
        "Casual":       ["super easy", "you will love", "pretty amazing"],
        "Urgent":       ["today only", "right now", "before it is gone"],
        "Inspirational":["transform", "elevate", "unlock your potential with"],
    }.get(tone, ["trusted", "powerful", "effective"])
    variants = []
    for i, tmpl in enumerate(TEMPLATE_AD_COPY[objective][:3]):
        mod = mods[i % len(mods)]
        variants.append({
            "headline":     tmpl["headline"].format(product=product[:18], modifier=mod, usp=usp[:20])[:40],
            "primary_text": tmpl["primary_text"].format(product=product, audience=audience, usp=usp, modifier=mod)[:125],
            "cta":          tmpl["cta"],
            "rationale":    tmpl["rationale"].format(objective=objective, tone=tone),
        })
    return variants


def render_ad_copy_tab():
    # Form
    col_main, col_side = st.columns([3, 2], gap="large")
    with col_main:
        product  = st.text_input("Product / Service", placeholder="e.g., CloudSync Pro")
        audience = st.text_input("Target Audience", placeholder="e.g., Small business owners aged 25 to 45")
        usp      = st.text_input("Key Selling Point", placeholder="e.g., Saves 5 hours per week")

    with col_side:
        objective = st.selectbox("Campaign Objective", ["Awareness", "Traffic", "Conversions", "Leads"])
        tone      = st.selectbox("Tone", ["Professional", "Casual", "Urgent", "Inspirational"])
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        generate  = st.button("Generate variants", type="primary", use_container_width=True)

    if generate:
        if not product or not audience or not usp:
            st.error("Fill in Product, Audience, and Selling Point to continue.")
            return

        with st.spinner("Writing your variants..."):
            client = get_anthropic_client()
            variants, used_ai = None, False
            if client:
                try:
                    variants = _call_ai_for_ad_copy(client, product, audience, objective, tone, usp)
                    used_ai = True
                except Exception as exc:
                    st.warning(f"AI unavailable ({str(exc)[:55]}). Falling back to templates.")
            if not variants:
                variants = _template_ad_copy(product, audience, objective, tone, usp)

        st.markdown(_thin_rule(), unsafe_allow_html=True)

        src_label = "Generated by claude-haiku-4-5" if used_ai else "Generated from templates"
        src_color = "#22C55E" if used_ai else "#6366F1"
        st.markdown(
            f'<span style="color:{src_color};font-size:0.73rem;font-weight:500;">{src_label}</span>',
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        nums   = ["01", "02", "03"]
        obj_c  = OBJECTIVE_COLORS.get(objective, ACCENT)

        for i, v in enumerate(variants):
            hl    = v.get("headline", "")
            pt    = v.get("primary_text", "")
            cta   = v.get("cta", "Learn More")
            rat   = v.get("rationale", "")
            hlen  = len(hl)
            ptlen = len(pt)
            hc    = "#22C55E" if hlen  <= 40  else "#EF4444"
            pc    = "#22C55E" if ptlen <= 125 else "#EF4444"

            st.markdown(f"""
<div style="padding:32px 0;border-bottom:1px solid rgba(255,255,255,0.05);">

  <div style="display:flex;align-items:center;gap:14px;margin-bottom:26px;">
    <span style="color:#FF5E2C;font-size:0.7rem;font-weight:700;letter-spacing:0.12em;flex-shrink:0;">{nums[i]}</span>
    <div style="height:1px;flex:1;background:rgba(255,255,255,0.05);"></div>
    <span style="color:#2E2E2E;font-size:0.65rem;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;">
      {objective} &nbsp;·&nbsp; {tone}
    </span>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:36px;margin-bottom:22px;">
    <div>
      <div style="color:#2E2E2E;font-size:0.65rem;font-weight:600;letter-spacing:0.12em;
      text-transform:uppercase;margin-bottom:10px;">
        Headline&nbsp;&nbsp;<span style="color:{hc};letter-spacing:0;">{hlen}/40</span>
      </div>
      <div style="color:#F0F0F0;font-size:1.08rem;font-weight:600;line-height:1.45;
      letter-spacing:-0.01em;">{hl}</div>
    </div>
    <div>
      <div style="color:#2E2E2E;font-size:0.65rem;font-weight:600;letter-spacing:0.12em;
      text-transform:uppercase;margin-bottom:10px;">
        Primary Text&nbsp;&nbsp;<span style="color:{pc};letter-spacing:0;">{ptlen}/125</span>
      </div>
      <div style="color:#888;font-size:0.875rem;line-height:1.7;">{pt}</div>
    </div>
  </div>

  <div style="display:flex;align-items:flex-start;gap:20px;">
    <div style="background:{obj_c};color:#fff;padding:9px 20px;border-radius:4px;
    font-size:0.8rem;font-weight:600;white-space:nowrap;flex-shrink:0;letter-spacing:0.01em;">
      {cta}
    </div>
    <div style="color:#303030;font-size:0.82rem;line-height:1.65;padding-top:8px;">
      {rat}
    </div>
  </div>

</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# TAB 2 — Campaign Performance Analyzer
# ---------------------------------------------------------------------------

def _metric_color(col, val):
    cfg = BENCHMARK_THRESHOLDS.get(col)
    if not cfg:
        return ""
    g, w, hi = cfg["good"], cfg["warn"], cfg["higher_is_better"]
    bg = (GREEN if (val >= g if hi else val <= g)
          else AMBER if (val >= w if hi else val <= w)
          else RED)
    return f"background-color:{bg};color:#fff;font-weight:600"


def _style_row(row):
    out = []
    for col in row.index:
        if col in BENCHMARK_THRESHOLDS:
            try:
                val = float(str(row[col]).replace("%","").replace("$","").replace(",","").strip())
                out.append(_metric_color(col, val))
            except (ValueError, TypeError):
                out.append("")
        else:
            out.append("")
    return out


def _analyze_with_ai(client, df_str):
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=900,
        messages=[{"role": "user", "content": (
            "You are a senior digital marketing analyst. Analyze this campaign data:\n\n"
            f"{df_str}\n\n"
            "Benchmarks: CTR > 1% good, ROAS > 2x profitable, CPC < $2 efficient, CPM < $5 efficient.\n\n"
            "Write three sections with markdown headers:\n"
            "**What is Working Well** (2-3 bullets with specific numbers)\n"
            "**What is Underperforming** (2-3 bullets with specific numbers)\n"
            "**Three Recommendations** (numbered, with expected impact)\n\n"
            "Reference campaign names and exact figures. No em dashes."
        )}],
    )
    return msg.content[0].text


def _analyze_with_rules(df):
    good, bad, recs = [], [], []
    for _, row in df.iterrows():
        name = row.get("Campaign", "This campaign")
        for col, hi, tg, tw, unit in [
            ("CTR (%)", True, 1.5, 0.8, "%"),
            ("ROAS",   True, 3.0, 1.5, "x"),
            ("CPC ($)", False, 1.5, 2.5, ""),
            ("CPM ($)", False, 4.0, 8.0, ""),
        ]:
            if col not in df.columns:
                continue
            try:
                val = float(str(row[col]).replace("$","").replace("%","").replace("x","").replace(",",""))
            except (ValueError, TypeError):
                continue
            if hi:
                if val >= tg:
                    good.append(f"{name} achieves {col} of {val:.2f}{unit} (benchmark: above {tg}{unit})")
                elif val < tw:
                    bad.append(f"{name} {col} of {val:.2f}{unit} is below the {tw}{unit} threshold")
                    if col == "CTR (%)":
                        recs.append(f"Refresh creatives for {name} to push CTR above 1%")
                    elif col == "ROAS":
                        recs.append(f"Improve bid strategy for {name} to reach 2x ROAS")
            else:
                if val <= tg:
                    good.append(f"{name} maintains efficient {col} at {val:.2f} (target: below {tg})")
                elif val > tw:
                    bad.append(f"{name} {col} of {val:.2f} exceeds the {tw} target")
                    if col == "CPC ($)":
                        recs.append(f"Narrow audience for {name} to bring CPC toward $1.50")

    if not good:
        good = [
            "All campaigns are generating impressions and measurable site traffic",
            "Spend is spread across campaigns, reducing single-channel risk",
        ]
    if not bad:
        bad = [
            "Minor efficiency gaps exist that bid adjustments can address",
            "Conversion volume has room to grow with audience refinement",
        ]
    recs = (recs + [
        "A/B test headlines across campaigns to target a 15 to 20% CTR lift",
        "Apply dayparting to concentrate budget on peak conversion hours",
        "Build lookalike audiences from top converters to improve ROAS",
    ])[:3]

    lines = ["**What is Working Well**"] + [f"- {p}" for p in good[:3]]
    lines += ["", "**What is Underperforming**"] + [f"- {p}" for p in bad[:3]]
    lines += ["", "**Three Recommendations**"] + [f"{i}. {r}" for i, r in enumerate(recs, 1)]
    return "\n".join(lines)


DEFAULT_CAMPAIGN_DATA = {
    "Campaign":    ["Brand Awareness Q4", "Lead Gen - Email List", "Retargeting - Abandoned Cart"],
    "Impressions": [450000, 120000, 85000],
    "Clicks":      [3150,   2040,   2125],
    "Conversions": [63,     204,    468],
    "Spend ($)":   [1800,   1560,   1275],
    "Reach":       [380000, 95000,  72000],
    "CTR (%)":     [0.70,   1.70,   2.50],
    "CPC ($)":     [0.57,   0.76,   0.60],
    "CPM ($)":     [4.00,   13.00,  15.00],
    "ROAS":        [1.75,   3.20,   5.50],
}


def render_performance_tab():
    method = st.radio("", ["Manual Entry", "Upload CSV"], horizontal=True, label_visibility="collapsed")
    df = None

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    if method == "Manual Entry":
        df = st.data_editor(
            pd.DataFrame(DEFAULT_CAMPAIGN_DATA),
            use_container_width=True,
            num_rows="dynamic",
            key="campaign_editor",
        )
    else:
        uploaded = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
        if uploaded:
            df = pd.read_csv(uploaded)
            st.dataframe(df, use_container_width=True)
        else:
            st.markdown(
                '<div style="color:#2E2E2E;font-size:0.82rem;padding:14px 0;">'
                'Expected columns: Campaign, Impressions, Clicks, Conversions, '
                'Spend ($), Reach, CTR (%), CPC ($), CPM ($), ROAS</div>',
                unsafe_allow_html=True,
            )

    if df is None or df.empty:
        return

    # Color-coded table
    st.markdown(_thin_rule(), unsafe_allow_html=True)
    st.markdown(
        '<div style="display:flex;gap:16px;align-items:center;margin-bottom:14px;">'
        f'<span style="color:#2E2E2E;font-size:0.68rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;">Performance Table</span>'
        '<div style="display:flex;gap:10px;margin-left:auto;">'
        f'<span style="color:{GREEN};font-size:0.7rem;font-weight:500;">● Strong</span>'
        f'<span style="color:{AMBER};font-size:0.7rem;font-weight:500;">● Watch</span>'
        f'<span style="color:{RED};font-size:0.7rem;font-weight:500;">● Below target</span>'
        '</div></div>',
        unsafe_allow_html=True,
    )
    try:
        st.dataframe(df.style.apply(_style_row, axis=1), use_container_width=True)
    except Exception:
        st.dataframe(df, use_container_width=True)

    # Aggregate KPI row — pure HTML numbers
    kpi_defs = [
        ("Avg CTR",     "CTR (%)",     lambda v: f"{v:.2f}%",   "benchmark: > 1.0%"),
        ("Avg CPC",     "CPC ($)",     lambda v: f"${v:.2f}",   "target: < $2.00"),
        ("Avg CPM",     "CPM ($)",     lambda v: f"${v:.2f}",   "target: < $5.00"),
        ("Avg ROAS",    "ROAS",        lambda v: f"{v:.2f}x",   "benchmark: > 2.0x"),
        ("Conversions", "Conversions", lambda v: f"{v:,.0f}",   "total across campaigns"),
    ]

    kpi_parts = []
    for label, col_name, fmt, bench in kpi_defs:
        if col_name not in df.columns:
            continue
        try:
            nums = pd.to_numeric(
                df[col_name].astype(str).str.replace(r"[$%x,]", "", regex=True), errors="coerce"
            )
            val = nums.sum() if "Conv" in label else nums.mean()
            # Color only the benchmark-tracked metrics
            cfg = BENCHMARK_THRESHOLDS.get(col_name)
            if cfg:
                g, w, hi = cfg["good"], cfg["warn"], cfg["higher_is_better"]
                vc = GREEN if (val >= g if hi else val <= g) else (AMBER if (val >= w if hi else val <= w) else RED)
            else:
                vc = "#E8E8E8"
            kpi_parts.append(
                f'<div style="border-right:1px solid rgba(255,255,255,0.05);padding-right:28px;margin-right:0;">'
                f'<div style="color:#303030;font-size:0.65rem;font-weight:600;letter-spacing:0.1em;'
                f'text-transform:uppercase;margin-bottom:8px;">{label}</div>'
                f'<div style="color:{vc};font-size:1.55rem;font-weight:700;letter-spacing:-0.025em;'
                f'font-variant-numeric:tabular-nums;margin-bottom:5px;">{fmt(val)}</div>'
                f'<div style="color:#242424;font-size:0.7rem;">{bench}</div>'
                f'</div>'
            )
        except Exception:
            pass

    if kpi_parts:
        st.markdown(_thin_rule(), unsafe_allow_html=True)
        st.markdown(
            f'<div style="display:grid;grid-template-columns:repeat({len(kpi_parts)},1fr);'
            f'gap:28px;padding:20px 0;">' + "".join(kpi_parts) + "</div>",
            unsafe_allow_html=True,
        )

    # ROAS chart
    if "ROAS" in df.columns and "Campaign" in df.columns:
        st.markdown(_thin_rule(), unsafe_allow_html=True)
        st.markdown(_label("ROAS vs 2x Benchmark"), unsafe_allow_html=True)
        try:
            roas_vals = pd.to_numeric(
                df["ROAS"].astype(str).str.replace(r"[x,]", "", regex=True), errors="coerce"
            ).tolist()
            campaigns = df["Campaign"].tolist()

            bar_colors = [ACCENT if v >= 2 else "#1E1E1E" for v in roas_vals]
            text_colors = [ACCENT if v >= 2 else "#444" for v in roas_vals]

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=roas_vals, y=campaigns,
                orientation="h",
                marker=dict(color=bar_colors, line=dict(width=0)),
                text=[f"{v:.2f}x" for v in roas_vals],
                textposition="outside",
                textfont=dict(size=12, color=text_colors),
                hovertemplate="%{y}: %{x:.2f}x ROAS<extra></extra>",
            ))
            fig.add_vline(
                x=2.0, line_dash="dot",
                line_color="rgba(255,255,255,0.12)", line_width=1.5,
                annotation_text="2x", annotation_font_color="#444",
                annotation_font_size=11, annotation_position="top right",
            )
            fig.update_layout(
                height=160 + len(campaigns) * 44,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(
                    showgrid=True, gridcolor="rgba(255,255,255,0.03)",
                    zeroline=False, color="#333", tickfont=dict(size=11),
                    title=None,
                ),
                yaxis=dict(
                    color="#777", automargin=True,
                    tickfont=dict(size=12),
                ),
                margin=dict(l=0, r=70, t=8, b=8),
                font=dict(color="#555", size=12),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            pass

    # AI analysis
    st.markdown(_thin_rule(), unsafe_allow_html=True)
    st.markdown(_label("Performance Analysis"), unsafe_allow_html=True)

    if st.button("Run analysis", type="primary"):
        with st.spinner("Analyzing..."):
            client = get_anthropic_client()
            df_str = df.to_string(index=False)
            if client:
                try:
                    analysis = _analyze_with_ai(client, df_str)
                    ai_label = "claude-haiku-4-5"
                except Exception as exc:
                    st.warning(f"AI unavailable ({str(exc)[:55]}). Using rule-based engine.")
                    analysis = _analyze_with_rules(df)
                    ai_label = None
            else:
                analysis = _analyze_with_rules(df)
                ai_label = None

        if ai_label:
            st.markdown(
                f'<span style="color:#22C55E;font-size:0.72rem;font-weight:500;">'
                f'Powered by {ai_label}</span>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<span style="color:#6366F1;font-size:0.72rem;font-weight:500;">Rule-based analysis</span>',
                unsafe_allow_html=True,
            )
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        st.markdown(f'<div class="analysis-text">', unsafe_allow_html=True)
        st.markdown(analysis)
        st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# TAB 3 — A/B Variant Scorer
# ---------------------------------------------------------------------------

def _score_clarity(h, b):
    s = 5.0
    wh = len(h.split())
    s += 2.0 if 4 <= wh <= 8 else (-1.0 if wh < 3 or wh > 12 else 0)
    wb = len(b.split())
    s += 2.0 if 15 <= wb <= 35 else (-2.0 if wb < 5 else (-1.0 if wb > 55 else 0))
    s += min(sum(1 for w in CLARITY_POSITIVE if w in b.lower()) * 0.5, 1.5)
    if "?" in h:
        s -= 0.5
    return min(max(round(s, 1), 0.0), 10.0)


def _score_urgency(h, b):
    s = 3.0
    c = (h + " " + b).lower()
    s += min(sum(1 for w in URGENCY_WORDS if w in c) * 1.2, 5.0)
    s += min(c.count("!") * 0.5, 1.5)
    if re.search(r"\d+", c):
        s += 0.5
    return min(max(round(s, 1), 0.0), 10.0)


def _score_relevance(h, b):
    s = 4.0
    c = (h + " " + b).lower()
    s += min(sum(1 for w in POWER_WORDS if w in c) * 0.6, 3.0)
    if re.search(r"\d+%|\d+x|\$\d+|\d+ hours|\d+ days|\d+ minutes", c):
        s += 1.5
    s += min(sum(1 for w in ["save","get","increase","reduce","improve","boost","gain","earn"] if w in c) * 0.5, 1.5)
    return min(max(round(s, 1), 0.0), 10.0)


def _score_cta(h, b):
    s = 3.0
    c = (h + " " + b).lower()
    s += min(sum(1 for kw in CTA_KEYWORDS if kw in c) * 1.5, 5.0)
    s += min(sum(1 for w in ["start","join","discover","unlock","claim","try","get","book","download"] if w in c) * 0.5, 1.5)
    if "you" in c or "your" in c:
        s += 0.5
    return min(max(round(s, 1), 0.0), 10.0)


def _overall(cl, ur, rv, ct):
    return round(cl * 0.30 + ur * 0.20 + rv * 0.30 + ct * 0.20, 1)


_V_COLORS = ["#FF5E2C", "#6366F1", "#10B981", "#F59E0B", "#8B5CF6"]
_V_FILL   = ["rgba(255,94,44,0.12)", "rgba(99,102,241,0.12)", "rgba(16,185,129,0.12)",
             "rgba(245,158,11,0.12)", "rgba(139,92,246,0.12)"]


def _bar_chart(results):
    fig = go.Figure()
    dims = ["Clarity", "Urgency", "Relevance", "CTA Strength"]
    for i, (_, row) in enumerate(results.iterrows()):
        fig.add_trace(go.Bar(
            name=row["Variant"],
            x=dims,
            y=[row[d] for d in dims],
            marker_color=_V_COLORS[i % len(_V_COLORS)],
            marker_opacity=0.85,
            text=[f"{row[d]:.1f}" for d in dims],
            textposition="outside",
            textfont=dict(size=11, color="#555"),
        ))
    fig.update_layout(
        barmode="group",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(color="#444", gridcolor="rgba(0,0,0,0)", tickfont=dict(size=12)),
        yaxis=dict(range=[0, 12], color="#333", gridcolor="rgba(255,255,255,0.03)",
                   tickfont=dict(size=11), title=None, zeroline=False),
        legend=dict(font=dict(color="#777", size=11), bgcolor="rgba(0,0,0,0)",
                    orientation="h", y=1.12, x=0),
        margin=dict(l=0, r=0, t=30, b=0),
        font=dict(color="#666", size=12),
        height=320,
    )
    return fig


def _radar_chart(results):
    dims = ["Clarity", "Urgency", "Relevance", "CTA Strength"]
    fig = go.Figure()
    for i, (_, row) in enumerate(results.iterrows()):
        vals = [row[d] for d in dims] + [row[dims[0]]]
        fig.add_trace(go.Scatterpolar(
            r=vals,
            theta=dims + [dims[0]],
            fill="toself",
            name=row["Variant"],
            line=dict(color=_V_COLORS[i % len(_V_COLORS)], width=2),
            fillcolor=_V_FILL[i % len(_V_FILL)],
        ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 10], color="#2E2E2E",
                            gridcolor="rgba(255,255,255,0.05)", tickfont=dict(size=9)),
            angularaxis=dict(color="#555", gridcolor="rgba(255,255,255,0.05)"),
        ),
        legend=dict(font=dict(color="#777", size=11), bgcolor="rgba(0,0,0,0)",
                    orientation="h", y=1.12, x=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#555", size=12),
        margin=dict(l=10, r=10, t=30, b=10),
        height=320,
    )
    return fig


def render_ab_scorer_tab():
    # Scoring key
    st.markdown(
        '<div style="display:flex;gap:28px;padding-bottom:24px;'
        'border-bottom:1px solid rgba(255,255,255,0.05);margin-bottom:28px;">'
        + "".join([
            f'<div><div style="color:#2E2E2E;font-size:0.65rem;font-weight:600;'
            f'letter-spacing:0.1em;text-transform:uppercase;margin-bottom:5px;">{n}</div>'
            f'<div style="color:#555;font-size:0.8rem;">{w}</div></div>'
            for n, w in [("Clarity","30%"), ("Relevance","30%"), ("Urgency","20%"), ("CTA Strength","20%")]
        ])
        + '</div>',
        unsafe_allow_html=True,
    )

    num_variants = st.slider("", min_value=2, max_value=5, value=2, label_visibility="collapsed")
    st.markdown(
        f'<span style="color:#2E2E2E;font-size:0.72rem;">{num_variants} variants selected</span>',
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    variants_input = []
    for i in range(num_variants):
        label = chr(65 + i)
        with st.expander(f"Variant {label}", expanded=(i < 2)):
            c1, c2 = st.columns(2, gap="medium")
            with c1:
                hl = st.text_input("Headline", key=f"ab_hl_{i}",
                                   placeholder="e.g., Save 3 Hours Daily with AI")
            with c2:
                bd = st.text_area("Ad Body", key=f"ab_bd_{i}",
                                  placeholder="e.g., Join 10,000 teams who automate their workflow. Start free today.",
                                  height=72)
        variants_input.append({"name": f"Variant {label}", "headline": hl, "body": bd})

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    if st.button("Score variants", type="primary", use_container_width=True):
        valid = [v for v in variants_input if v["headline"] and v["body"]]
        if len(valid) < 2:
            st.error("Enter at least 2 complete variants to score.")
            return

        rows = []
        for v in valid:
            cl = _score_clarity(v["headline"], v["body"])
            ur = _score_urgency(v["headline"], v["body"])
            rv = _score_relevance(v["headline"], v["body"])
            ct = _score_cta(v["headline"], v["body"])
            ov = _overall(cl, ur, rv, ct)
            rows.append({"Variant": v["name"], "Clarity": cl, "Urgency": ur,
                         "Relevance": rv, "CTA Strength": ct, "Overall": ov})

        results = pd.DataFrame(rows).sort_values("Overall", ascending=False).reset_index(drop=True)

        st.markdown(_thin_rule(), unsafe_allow_html=True)

        # Score table — inline HTML for clean look
        score_cols = ["Clarity", "Urgency", "Relevance", "CTA Strength", "Overall"]

        def _cell(val, is_overall=False):
            c = (GREEN if val >= 7 else AMBER if val >= 5 else RED)
            size = "0.98rem" if is_overall else "0.88rem"
            weight = "700" if is_overall else "500"
            return (f'<td style="padding:12px 16px;color:{c};font-size:{size};'
                    f'font-weight:{weight};font-variant-numeric:tabular-nums;">{val:.1f}</td>')

        header_cells = ('<th style="padding:10px 16px;color:#2E2E2E;font-size:0.65rem;font-weight:600;'
                       'letter-spacing:0.1em;text-transform:uppercase;text-align:left;">Variant</th>'
                       + "".join(
                           f'<th style="padding:10px 16px;color:#2E2E2E;font-size:0.65rem;font-weight:600;'
                           f'letter-spacing:0.1em;text-transform:uppercase;">{col}</th>'
                           for col in score_cols
                       ))
        rows_html = ""
        for i, (_, row) in enumerate(results.iterrows()):
            vc = _V_COLORS[i % len(_V_COLORS)]
            rows_html += (
                f'<tr style="border-bottom:1px solid rgba(255,255,255,0.04);">'
                f'<td style="padding:12px 16px;">'
                f'<span style="display:inline-flex;align-items:center;gap:7px;">'
                f'<span style="width:7px;height:7px;border-radius:50%;background:{vc};flex-shrink:0;"></span>'
                f'<span style="color:#CCC;font-size:0.875rem;font-weight:500;">{row["Variant"]}</span>'
                f'</span></td>'
                + _cell(row["Clarity"])
                + _cell(row["Urgency"])
                + _cell(row["Relevance"])
                + _cell(row["CTA Strength"])
                + _cell(row["Overall"], is_overall=True)
                + '</tr>'
            )

        st.markdown(
            f'<table style="width:100%;border-collapse:collapse;background:#0C0C0C;'
            f'border:1px solid rgba(255,255,255,0.06);border-radius:6px;overflow:hidden;">'
            f'<thead style="border-bottom:1px solid rgba(255,255,255,0.06);">'
            f'<tr>{header_cells}</tr></thead>'
            f'<tbody>{rows_html}</tbody></table>',
            unsafe_allow_html=True,
        )

        # Charts
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        chart_col, radar_col = st.columns(2, gap="large")
        with chart_col:
            st.markdown(_label("Score by Dimension"), unsafe_allow_html=True)
            st.plotly_chart(_bar_chart(results), use_container_width=True)
        with radar_col:
            st.markdown(_label("Radar Comparison"), unsafe_allow_html=True)
            st.plotly_chart(_radar_chart(results), use_container_width=True)

        # Recommendation
        winner = results.iloc[0]
        runner = results.iloc[1] if len(results) > 1 else None
        best   = max(["Clarity", "Urgency", "Relevance", "CTA Strength"], key=lambda d: winner[d])
        gap    = winner["Overall"] - runner["Overall"] if runner is not None else 0

        rec = (f"{winner['Variant']} scores highest at {winner['Overall']:.1f}/10, "
               f"leading on {best} ({winner[best]:.1f}/10).")
        if runner is not None:
            rec += (f" Test it first." if gap >= 0.5 else
                    f" {runner['Variant']} ({runner['Overall']:.1f}/10) is close enough to run as a direct challenger.")

        st.markdown(_thin_rule(), unsafe_allow_html=True)
        vc = _V_COLORS[0]
        st.markdown(
            f'<div style="padding:4px 0 24px;">'
            f'<div style="color:#2E2E2E;font-size:0.65rem;font-weight:600;letter-spacing:0.12em;'
            f'text-transform:uppercase;margin-bottom:12px;">Recommendation</div>'
            f'<div style="font-size:1.0rem;color:#CCC;line-height:1.7;max-width:700px;">'
            f'<span style="color:{vc};font-weight:600;">{winner["Variant"]}</span> {rec[len(winner["Variant"]):]}'
            f'</div></div>',
            unsafe_allow_html=True,
        )

        # Per-variant breakdown with st.metric
        st.markdown(_label("Dimension Breakdown"), unsafe_allow_html=True)
        metric_cols = st.columns(len(valid), gap="large")
        for col_w, (_, row) in zip(metric_cols, results.iterrows()):
            col_w.markdown(
                f'<span style="color:#888;font-size:0.8rem;font-weight:600;">{row["Variant"]}</span>',
                unsafe_allow_html=True,
            )
            col_w.metric("Clarity",      f"{row['Clarity']}/10")
            col_w.metric("Urgency",      f"{row['Urgency']}/10")
            col_w.metric("Relevance",    f"{row['Relevance']}/10")
            col_w.metric("CTA Strength", f"{row['CTA Strength']}/10")
            col_w.metric("Overall",      f"{row['Overall']}/10")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    inject_css()

    # Sidebar
    with st.sidebar:
        client = get_anthropic_client()

        st.markdown(
            '<div style="margin-bottom:24px;padding-bottom:20px;'
            'border-bottom:1px solid rgba(255,255,255,0.05);">'
            '<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">'
            '<span style="color:#FF5E2C;font-weight:800;font-size:0.95rem;">◆</span>'
            '<span style="color:#E8E8E8;font-size:0.9rem;font-weight:700;letter-spacing:-0.01em;">Marketing AI</span>'
            '</div>'
            '<span style="color:#1E1E1E;font-size:0.72rem;padding-left:20px;">Platform v1.0</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        if client:
            st.markdown(
                '<div style="display:flex;align-items:center;gap:7px;margin-bottom:20px;">'
                '<div style="width:6px;height:6px;border-radius:50%;background:#22C55E;flex-shrink:0;"></div>'
                '<span style="color:#22C55E;font-size:0.78rem;font-weight:500;">API connected</span>'
                '</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="display:flex;align-items:center;gap:7px;margin-bottom:10px;">'
                '<div style="width:6px;height:6px;border-radius:50%;background:#F59E0B;flex-shrink:0;"></div>'
                '<span style="color:#F59E0B;font-size:0.78rem;font-weight:500;">API not configured</span>'
                '</div>'
                '<div style="color:#242424;font-size:0.73rem;line-height:1.65;margin-bottom:20px;'
                'padding:10px 12px;background:#0A0A0A;border-radius:4px;border:1px solid rgba(255,255,255,0.05);">'
                'Add <code style="color:#555;font-size:0.72rem;">ANTHROPIC_API_KEY</code> to Streamlit secrets. '
                'All tabs work without it.'
                '</div>',
                unsafe_allow_html=True,
            )

        info = [("Model", "claude-haiku-4-5"), ("Framework", "Streamlit"), ("Charts", "Plotly")]
        for lbl, val in info:
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'padding:7px 0;border-bottom:1px solid rgba(255,255,255,0.04);">'
                f'<span style="color:#242424;font-size:0.73rem;">{lbl}</span>'
                f'<span style="color:#484848;font-size:0.73rem;font-weight:500;">{val}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            '<div style="margin-top:28px;padding-top:20px;border-top:1px solid rgba(255,255,255,0.04);">'
            '<div style="color:#3A3A3A;font-size:0.75rem;font-weight:600;margin-bottom:5px;">Ridhan Parvendhan</div>'
            '<div style="color:#1E1E1E;font-size:0.72rem;line-height:1.6;">'
            'All sample data is synthetic and for demonstration only.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    # Page header
    st.markdown(
        '<div style="padding-bottom:28px;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:32px;">'
        '<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">'
        '<span style="color:#FF5E2C;font-size:0.95rem;font-weight:800;">◆</span>'
        '<span style="color:#F5F5F5;font-size:1.45rem;font-weight:700;letter-spacing:-0.025em;">Marketing AI Platform</span>'
        '</div>'
        '<p style="margin:0;color:#3A3A3A;font-size:0.85rem;line-height:1.6;max-width:540px;">'
        'AI-powered tools for ad creation, campaign analysis, and copy variant scoring.'
        '</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["Ad Copy Generator", "Campaign Analyzer", "A/B Variant Scorer"])
    with tab1:
        render_ad_copy_tab()
    with tab2:
        render_performance_tab()
    with tab3:
        render_ab_scorer_tab()


if __name__ == "__main__":
    main()
