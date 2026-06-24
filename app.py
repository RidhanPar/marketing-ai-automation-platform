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

ACCENT = "#FF6B3B"
GREEN  = "#22C55E"
AMBER  = "#F59E0B"
RED    = "#EF4444"

OBJECTIVE_COLORS = {
    "Awareness":   "#6366F1",
    "Traffic":     "#10B981",
    "Conversions": "#FF6B3B",
    "Leads":       "#8B5CF6",
}

# ---------------------------------------------------------------------------
# CSS injection
# ---------------------------------------------------------------------------

def inject_css():
    st.markdown(
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">',
        unsafe_allow_html=True,
    )

    css = (
        "*, *::before, *::after { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }"
        "#MainMenu, footer, header { visibility: hidden; }"
        ".block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1140px !important; }"

        # App shell
        ".stApp { background: #080808 !important; }"

        # Sidebar
        "[data-testid='stSidebar'] { background: #040404 !important; border-right: 1px solid #141414 !important; }"
        "[data-testid='stSidebar'] .block-container { padding: 1.75rem 1.25rem 1.5rem !important; }"

        # Tab bar - underline only, no pill/card
        ".stTabs [data-baseweb='tab-list'] { background: transparent !important; border: none !important; border-bottom: 1px solid #1E1E1E !important; border-radius: 0 !important; padding: 0 !important; gap: 0 !important; margin-bottom: 40px !important; }"
        ".stTabs [data-baseweb='tab'] { background: transparent !important; border-radius: 0 !important; color: #888 !important; font-size: 0.84rem !important; font-weight: 400 !important; padding: 13px 0 !important; margin-right: 30px !important; border-bottom: 2px solid transparent !important; margin-bottom: -1px !important; letter-spacing: 0.01em !important; transition: color 0.12s !important; }"
        ".stTabs [data-baseweb='tab']:hover { color: #CCC !important; }"
        ".stTabs [aria-selected='true'] { color: #EFEFEF !important; font-weight: 600 !important; border-bottom-color: #FF6B3B !important; background: transparent !important; }"
        ".stTabs [data-baseweb='tab-highlight'], .stTabs [data-baseweb='tab-border'] { display: none !important; }"

        # Inputs
        ".stTextInput input, .stTextArea textarea { background: #0E0E0E !important; border: 1px solid #222 !important; border-radius: 6px !important; color: #E8E8E8 !important; font-size: 0.875rem !important; caret-color: #FF6B3B !important; transition: border-color 0.12s !important; padding: 9px 12px !important; }"
        ".stTextInput input:focus, .stTextArea textarea:focus { border-color: rgba(255,107,59,0.5) !important; box-shadow: 0 0 0 3px rgba(255,107,59,0.06) !important; }"
        ".stTextInput input::placeholder, .stTextArea textarea::placeholder { color: #444 !important; }"
        ".stTextInput label, .stTextArea label { color: #A0A0A0 !important; font-size: 0.68rem !important; font-weight: 600 !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; margin-bottom: 6px !important; }"

        # Selectbox
        ".stSelectbox [data-baseweb='select'] > div:first-child { background: #0E0E0E !important; border: 1px solid #222 !important; border-radius: 6px !important; transition: border-color 0.12s !important; }"
        ".stSelectbox [data-baseweb='select'] > div:first-child:hover { border-color: #333 !important; }"
        ".stSelectbox label { color: #A0A0A0 !important; font-size: 0.68rem !important; font-weight: 600 !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; margin-bottom: 6px !important; }"
        ".stSelectbox svg { color: #888 !important; }"

        # Buttons
        ".stButton > button { border-radius: 6px !important; font-size: 0.875rem !important; font-weight: 500 !important; letter-spacing: 0.01em !important; transition: all 0.1s !important; height: 38px !important; }"
        ".stButton > button[kind='primary'] { background: #FF6B3B !important; border: none !important; color: #fff !important; }"
        ".stButton > button[kind='primary']:hover { background: #E85A2A !important; }"
        ".stButton > button[kind='secondary'] { background: transparent !important; border: 1px solid #222 !important; color: #777 !important; }"
        ".stButton > button[kind='secondary']:hover { border-color: #333 !important; color: #AAA !important; }"

        # Radio
        ".stRadio label span { color: #AAAAAA !important; font-size: 0.84rem !important; }"
        ".stRadio > div { gap: 4px !important; }"

        # Slider
        ".stSlider label { color: #A0A0A0 !important; font-size: 0.68rem !important; font-weight: 600 !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; }"
        ".stSlider [data-testid='stThumbValue'] { color: #FF6B3B !important; font-weight: 600 !important; }"
        ".stSlider [data-testid='stTickBar'] { color: #444 !important; }"

        # Expander
        "[data-testid='stExpander'] { background: #0B0B0B !important; border: 1px solid #1A1A1A !important; border-radius: 7px !important; margin-bottom: 8px !important; overflow: hidden !important; }"
        "[data-testid='stExpander'] summary { color: #BDBDBD !important; font-weight: 500 !important; font-size: 0.875rem !important; padding: 12px 16px !important; list-style: none !important; }"
        "[data-testid='stExpander'] summary:hover { color: #E8E8E8 !important; }"
        "[data-testid='stExpander'] summary svg { display: inline-block !important; vertical-align: middle !important; }"

        # Metric
        "[data-testid='stMetric'] { background: transparent !important; border: none !important; padding: 0 !important; }"
        "[data-testid='stMetricLabel'] p { color: #A0A0A0 !important; font-size: 0.67rem !important; font-weight: 600 !important; letter-spacing: 0.12em !important; text-transform: uppercase !important; }"
        "[data-testid='stMetricValue'] { color: #E2E2E2 !important; font-size: 1.5rem !important; font-weight: 700 !important; letter-spacing: -0.025em !important; font-variant-numeric: tabular-nums !important; }"

        # DataFrame
        "[data-testid='stDataFrameContainer'] { border: 1px solid #1A1A1A !important; border-radius: 7px !important; overflow: hidden !important; }"

        # File uploader
        "[data-testid='stFileUploaderDropzone'] { background: #0B0B0B !important; border: 1px dashed #222 !important; border-radius: 7px !important; }"

        # Alerts
        "[data-testid='stAlert'] { border-radius: 6px !important; }"

        # Divider
        "hr { border-color: #1A1A1A !important; margin: 32px 0 !important; }"

        # Scrollbars
        "::-webkit-scrollbar { width: 4px; height: 4px; }"
        "::-webkit-scrollbar-track { background: transparent; }"
        "::-webkit-scrollbar-thumb { background: #222; border-radius: 3px; }"
        "::-webkit-scrollbar-thumb:hover { background: #333; }"

        # Utility classes
        ".eyebrow { display: block; color: #FF6B3B; font-size: 0.64rem; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 16px; }"
        ".analysis-out p, .analysis-out li { color: #A8A8A8; font-size: 0.875rem; line-height: 1.8; margin: 0 0 4px; }"
        ".analysis-out strong { color: #D8D8D8; }"
        ".analysis-out h2, .analysis-out h3 { color: #FF6B3B; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin: 22px 0 10px; }"
    )

    components.html(
        f"""<script>
(function(){{
  var d=window.parent.document, id='mktai-v3';
  if(d.getElementById(id))return;
  var s=d.createElement('style'); s.id=id;
  s.textContent={json.dumps(css)};
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


def _eyebrow(text):
    st.markdown(f'<span class="eyebrow">{text}</span>', unsafe_allow_html=True)


def _sep(color="#141414"):
    st.markdown(f'<hr style="border-color:{color};margin:28px 0;">', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# TAB 1 - Ad Copy Generator
# ---------------------------------------------------------------------------

def _call_ai_for_ad_copy(client, product, audience, objective, tone, usp):
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": (
                f"You are an expert digital marketing copywriter. Generate 3 distinct ad copy variants.\n\n"
                f"Product: {product}\nAudience: {audience}\nObjective: {objective}\nTone: {tone}\nUSP: {usp}\n\n"
                f"Return ONLY a JSON array of 3 objects with keys: headline (max 40 chars), "
                f"primary_text (max 125 chars), cta (2-4 words), rationale (1 sentence). No em dashes."
            ),
        }],
    )
    text = msg.content[0].text
    m = re.search(r"\[.*\]", text, re.DOTALL)
    return json.loads(m.group())[:3] if m else None


def _template_ad_copy(product, audience, objective, tone, usp):
    tone_map = {
        "Professional": ["industry-leading", "enterprise-grade", "proven"],
        "Casual": ["super easy", "you will love", "pretty amazing"],
        "Urgent": ["today only", "right now", "before it is gone"],
        "Inspirational": ["transform", "elevate", "unlock your potential with"],
    }
    mods = tone_map.get(tone, ["trusted", "powerful", "effective"])
    out = []
    for i, tmpl in enumerate(TEMPLATE_AD_COPY[objective][:3]):
        m = mods[i % len(mods)]
        out.append({
            "headline": tmpl["headline"].format(product=product[:18], modifier=m, usp=usp[:20])[:40],
            "primary_text": tmpl["primary_text"].format(product=product, audience=audience, usp=usp, modifier=m)[:125],
            "cta": tmpl["cta"],
            "rationale": tmpl["rationale"].format(objective=objective, tone=tone),
        })
    return out


def render_ad_copy_tab():
    _eyebrow("Campaign Brief")

    col_l, col_r = st.columns([3, 2], gap="large")
    with col_l:
        product  = st.text_input("Product or Service", placeholder="CloudSync Pro")
        audience = st.text_input("Target Audience", placeholder="Small business owners aged 25 to 45")
        usp      = st.text_input("Key Selling Point", placeholder="Saves 5 hours per week")
    with col_r:
        objective = st.selectbox("Campaign Objective", ["Awareness", "Traffic", "Conversions", "Leads"])
        tone      = st.selectbox("Tone", ["Professional", "Casual", "Urgent", "Inspirational"])

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    generate = st.button("Generate Ad Copy", type="primary", use_container_width=True)

    if not generate:
        return

    if not (product and audience and usp):
        st.error("Please fill in Product, Audience, and Key Selling Point.")
        return

    with st.spinner("Writing variants..."):
        client = get_anthropic_client()
        variants, used_ai = None, False
        if client:
            try:
                variants = _call_ai_for_ad_copy(client, product, audience, objective, tone, usp)
                used_ai = True
            except Exception as exc:
                st.warning(f"AI unavailable ({str(exc)[:55]}). Using template engine.")
        if not variants:
            variants = _template_ad_copy(product, audience, objective, tone, usp)

    _sep()
    _eyebrow("Generated Variants")

    obj_color = OBJECTIVE_COLORS.get(objective, ACCENT)
    source_label = "AI" if used_ai else "Template"
    source_color = GREEN if used_ai else "#555"

    st.markdown(
        f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:28px;">'
        f'<span style="color:#FF6B3B;font-size:0.78rem;font-weight:700;letter-spacing:0.08em;">SOURCE</span>'
        f'<span style="color:{source_color};font-size:0.78rem;font-weight:600;">{source_label}</span>'
        f'<span style="color:#444;font-size:0.78rem;">|</span>'
        f'<span style="color:#A0A0A0;font-size:0.78rem;">Objective:</span>'
        f'<span style="color:{obj_color};font-size:0.78rem;font-weight:600;">{objective}</span>'
        f'<span style="color:#444;font-size:0.78rem;">|</span>'
        f'<span style="color:#A0A0A0;font-size:0.78rem;">Tone:</span>'
        f'<span style="color:#CCC;font-size:0.78rem;font-weight:500;">{tone}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    for idx, v in enumerate(variants):
        hl   = v.get("headline", "")
        pt   = v.get("primary_text", "")
        cta  = v.get("cta", "Learn More")
        rat  = v.get("rationale", "")
        hlen = len(hl)
        plen = len(pt)
        h_ok  = hlen <= 40
        pt_ok = plen <= 125

        h_count_style  = f"color:{'#888' if h_ok else RED}"
        pt_count_style = f"color:{'#888' if pt_ok else RED}"

        num_label = f"0{idx + 1}"

        st.markdown(
            f'<div style="display:grid;grid-template-columns:36px 1fr;gap:0;border-top:1px solid #141414;'
            f'padding:28px 0;">'

            # Left: number
            f'<div style="padding-top:2px;">'
            f'<span style="color:#666;font-size:0.72rem;font-weight:700;font-variant-numeric:tabular-nums;">{num_label}</span>'
            f'</div>'

            # Right: content
            f'<div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr auto;gap:24px;align-items:start;">'

            # Headline
            f'<div>'
            f'<div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:7px;">'
            f'<span style="color:#FF6B3B;font-size:0.67rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;">Headline</span>'
            f'<span style="{h_count_style};font-size:0.67rem;font-variant-numeric:tabular-nums;">{hlen}/40</span>'
            f'</div>'
            f'<div style="background:#0C0C0C;border:1px solid #171717;border-radius:5px;padding:10px 13px;'
            f'font-size:0.875rem;color:#E0E0E0;font-weight:500;line-height:1.5;min-height:42px;">{hl}</div>'
            f'</div>'

            # Primary text
            f'<div>'
            f'<div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:7px;">'
            f'<span style="color:#FF6B3B;font-size:0.67rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;">Primary Text</span>'
            f'<span style="{pt_count_style};font-size:0.67rem;font-variant-numeric:tabular-nums;">{plen}/125</span>'
            f'</div>'
            f'<div style="background:#0C0C0C;border:1px solid #171717;border-radius:5px;padding:10px 13px;'
            f'font-size:0.875rem;color:#C0C0C0;line-height:1.5;min-height:42px;">{pt}</div>'
            f'</div>'

            # CTA
            f'<div>'
            f'<div style="margin-bottom:7px;">'
            f'<span style="color:#FF6B3B;font-size:0.67rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;">CTA</span>'
            f'</div>'
            f'<button style="background:{obj_color};color:#fff;border:none;border-radius:6px;'
            f'padding:10px 18px;font-size:0.8rem;font-weight:600;white-space:nowrap;cursor:default;'
            f'font-family:Inter,sans-serif;letter-spacing:0.01em;">{cta}</button>'
            f'</div>'

            f'</div>'

            # Rationale
            f'<div style="margin-top:14px;padding-top:14px;border-top:1px solid #0F0F0F;">'
            f'<span style="color:#FF6B3B;font-size:0.67rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;">WHY IT WORKS</span>'
            f'<p style="color:#A8A8A8;font-size:0.835rem;line-height:1.7;margin:6px 0 0;">{rat}</p>'
            f'</div>'

            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div style="border-top:1px solid #141414;margin-top:4px;"></div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# TAB 2 - Campaign Performance Analyzer
# ---------------------------------------------------------------------------

def _metric_color(col_name, value):
    cfg = BENCHMARK_THRESHOLDS.get(col_name)
    if not cfg:
        return ""
    hi = cfg["higher_is_better"]
    bg = (GREEN if (value >= cfg["good"] if hi else value <= cfg["good"])
          else AMBER if (value >= cfg["warn"] if hi else value <= cfg["warn"])
          else RED)
    return f"background-color:{bg};color:#fff;font-weight:600"


def _style_row(row):
    out = []
    for col in row.index:
        if col in BENCHMARK_THRESHOLDS:
            try:
                val = float(str(row[col]).replace("%","").replace("$","").replace(",","").replace("x","").strip())
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
        messages=[{
            "role": "user",
            "content": (
                "You are a senior digital marketing analyst. Analyze this campaign data:\n\n"
                f"{df_str}\n\n"
                "Benchmarks: CTR > 1% good, ROAS > 2x profitable, CPC < $2 efficient, CPM < $5 efficient.\n\n"
                "Write three sections with markdown headers:\n"
                "### What is Working Well\n"
                "### What is Underperforming\n"
                "### Three Actionable Recommendations\n\n"
                "Be specific. Use campaign names and exact numbers. No em dashes."
            ),
        }],
    )
    return msg.content[0].text


def _analyze_with_rules(df):
    good, bad, recs = [], [], []
    for _, row in df.iterrows():
        name = row.get("Campaign", "This campaign")
        for col, hi, tg, tw in [
            ("CTR (%)", True, 1.5, 0.8), ("ROAS", True, 3.0, 1.5),
            ("CPC ($)", False, 1.5, 2.5), ("CPM ($)", False, 4.0, 8.0),
        ]:
            if col not in df.columns:
                continue
            try:
                v = float(str(row[col]).replace("$","").replace("%","").replace("x","").replace(",",""))
            except (ValueError, TypeError):
                continue
            if hi:
                if v >= tg:
                    good.append(f"{name} achieves {col} of {v:.2f} (benchmark above {tg})")
                elif v < tw:
                    bad.append(f"{name} {col} of {v:.2f} is below the {tw} threshold")
                    recs.append(f"Refresh creatives for {name} to lift CTR above 1%" if col == "CTR (%)" else f"Tighten bidding for {name} to reach 2x ROAS")
            else:
                if v <= tg:
                    good.append(f"{name} keeps {col} efficient at {v:.2f}")
                elif v > tw:
                    bad.append(f"{name} {col} of {v:.2f} exceeds the {tw} target")
                    recs.append(f"Narrow audience for {name} to bring CPC toward $1.50" if col == "CPC ($)" else f"Broaden targeting for {name} to lower CPM below $5")

    if not good:
        good = ["All campaigns are generating measurable impressions and traffic",
                "Spend is diversified across campaigns, reducing single-channel risk"]
    if not bad:
        bad = ["Minor efficiency gaps that targeted bid adjustments can address",
               "Conversion volume can improve with audience refinement"]
    recs = (recs + [
        "A/B test headlines to target a 15 to 20% CTR improvement",
        "Apply dayparting to concentrate budget on peak conversion hours",
        "Build lookalike audiences from your top 10% converters to lift ROAS",
    ])[:3]

    lines = ["### What is Working Well"] + [f"- {p}" for p in good[:3]]
    lines += ["", "### What is Underperforming"] + [f"- {p}" for p in bad[:3]]
    lines += ["", "### Three Actionable Recommendations"] + [f"{i}. {r}" for i, r in enumerate(recs, 1)]
    return "\n".join(lines)


DEFAULT_DATA = {
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


def render_performance_tab():
    _eyebrow("Campaign Data")

    method = st.radio("", ["Manual Entry", "Upload CSV"], horizontal=True, label_visibility="collapsed")
    df = None

    if method == "Manual Entry":
        df = st.data_editor(pd.DataFrame(DEFAULT_DATA), use_container_width=True, num_rows="dynamic", key="ce")
    else:
        up = st.file_uploader("Upload CSV", type=["csv"])
        if up:
            df = pd.read_csv(up)
            st.dataframe(df, use_container_width=True)
        else:
            st.markdown(
                '<p style="color:#A0A0A0;font-size:0.84rem;">Expected columns: Campaign, Impressions, Clicks, Conversions, Spend ($), Reach, CTR (%), CPC ($), CPM ($), ROAS</p>',
                unsafe_allow_html=True,
            )

    if df is None or df.empty:
        return

    _sep()

    # KPI strip
    _eyebrow("Aggregate Performance")
    kpi_defs = [
        ("Avg CTR", "CTR (%)", "CTR (%)", lambda v: f"{v:.2f}%"),
        ("Avg CPC", "CPC ($)", "CPC ($)", lambda v: f"${v:.2f}"),
        ("Avg CPM", "CPM ($)", "CPM ($)", lambda v: f"${v:.2f}"),
        ("Avg ROAS", "ROAS", "ROAS", lambda v: f"{v:.2f}x"),
        ("Total Conv.", "Conversions", None, lambda v: f"{v:,.0f}"),
    ]
    kpi_cols = st.columns(5, gap="large")
    kpi_vals = {}
    for col_w, (label, src_col, bench_col, fmt) in zip(kpi_cols, kpi_defs):
        if src_col not in df.columns:
            continue
        try:
            nums = pd.to_numeric(df[src_col].astype(str).str.replace(r"[$%x,]","",regex=True), errors="coerce")
            val = nums.sum() if "Conv" in label else nums.mean()
            kpi_vals[src_col] = val

            # Color based on benchmark
            val_color = "#E2E2E2"
            if bench_col and bench_col in BENCHMARK_THRESHOLDS:
                cfg = BENCHMARK_THRESHOLDS[bench_col]
                hi = cfg["higher_is_better"]
                val_color = (GREEN if (val >= cfg["good"] if hi else val <= cfg["good"])
                             else AMBER if (val >= cfg["warn"] if hi else val <= cfg["warn"])
                             else RED)

            col_w.markdown(
                f'<div>'
                f'<div style="color:#FF6B3B;font-size:0.64rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:6px;">{label}</div>'
                f'<div style="color:{val_color};font-size:1.55rem;font-weight:700;letter-spacing:-0.025em;font-variant-numeric:tabular-nums;line-height:1;">{fmt(val)}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        except Exception:
            pass

    _sep()

    # Color-coded table
    _eyebrow("Performance Breakdown")
    st.markdown(
        '<div style="display:flex;gap:16px;margin-bottom:14px;align-items:center;">'
        f'<span style="color:#FF6B3B;font-size:0.72rem;font-weight:700;letter-spacing:0.08em;">COLOR KEY</span>'
        f'<span style="display:flex;align-items:center;gap:5px;color:{GREEN};font-size:0.72rem;font-weight:600;">'
        f'<span style="width:6px;height:6px;background:{GREEN};border-radius:50%;display:inline-block;"></span>Strong</span>'
        f'<span style="display:flex;align-items:center;gap:5px;color:{AMBER};font-size:0.72rem;font-weight:600;">'
        f'<span style="width:6px;height:6px;background:{AMBER};border-radius:50%;display:inline-block;"></span>Needs work</span>'
        f'<span style="display:flex;align-items:center;gap:5px;color:{RED};font-size:0.72rem;font-weight:600;">'
        f'<span style="width:6px;height:6px;background:{RED};border-radius:50%;display:inline-block;"></span>Underperforming</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    try:
        st.dataframe(df.style.apply(_style_row, axis=1), use_container_width=True)
    except Exception:
        st.dataframe(df, use_container_width=True)

    # ROAS chart
    if "ROAS" in df.columns and "Campaign" in df.columns:
        _sep()
        _eyebrow("ROAS vs 2x Benchmark")
        try:
            roas_raw = pd.to_numeric(df["ROAS"].astype(str).str.replace(r"[x,]","",regex=True), errors="coerce")
            bar_c = [GREEN if v >= 2 else (AMBER if v >= 1.5 else RED) for v in roas_raw]
            fig = go.Figure(go.Bar(
                x=roas_raw.tolist(), y=df["Campaign"].tolist(), orientation="h",
                marker_color=bar_c,
                text=[f"{v:.2f}x" for v in roas_raw],
                textposition="outside", textfont=dict(color="#555", size=12, family="Inter"),
                hovertemplate="%{y}: %{x:.2f}x<extra></extra>",
            ))
            fig.add_vline(x=2.0, line_dash="dot", line_color="#333", line_width=1.5,
                          annotation_text="2x target", annotation_font_color="#777",
                          annotation_position="top right", annotation_font_size=11)
            fig.update_layout(
                height=48 * len(df) + 90,
                margin=dict(l=0, r=70, t=0, b=24),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(color="#555", gridcolor="#111", tickfont=dict(size=11, family="Inter"),
                           title=dict(text="", font=dict(color="#555")),
                           range=[0, max(roas_raw.max() * 1.3, 3.5)]),
                yaxis=dict(color="#888", tickfont=dict(size=12, family="Inter"), automargin=True),
                font=dict(color="#555", family="Inter"), showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        except Exception:
            pass

    _sep()
    _eyebrow("AI Analysis")

    if st.button("Analyze Campaign Performance", type="primary"):
        with st.spinner("Analyzing..."):
            client = get_anthropic_client()
            if client:
                try:
                    analysis = _analyze_with_ai(client, df.to_string(index=False))
                    badge = f'<span style="color:{GREEN};font-size:0.72rem;font-weight:600;">claude-haiku-4-5</span>'
                except Exception as exc:
                    st.warning(str(exc)[:60])
                    analysis = _analyze_with_rules(df)
                    badge = f'<span style="color:#444;font-size:0.72rem;font-weight:600;">Rule engine</span>'
            else:
                analysis = _analyze_with_rules(df)
                badge = f'<span style="color:#444;font-size:0.72rem;font-weight:600;">Rule engine</span>'

        st.markdown(
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:20px;">'
            f'<span style="color:#FF6B3B;font-size:0.64rem;font-weight:700;letter-spacing:0.12em;">POWERED BY</span>'
            f'{badge}</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="analysis-out">', unsafe_allow_html=True)
        st.markdown(analysis)
        st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# TAB 3 - A/B Variant Scorer
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
    if re.search(r"\d+%|\d+x|\$\d+|\d+ hours|\d+ days|\d+ min", c):
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


def _score_bar_html(label, score, color):
    pct = int(score * 10)
    return (
        f'<div style="display:grid;grid-template-columns:90px 1fr 32px;gap:10px;align-items:center;margin-bottom:8px;">'
        f'<span style="color:#A0A0A0;font-size:0.72rem;font-weight:500;">{label}</span>'
        f'<div style="height:3px;background:#111;border-radius:2px;overflow:hidden;">'
        f'<div style="height:100%;width:{pct}%;background:{color};border-radius:2px;transition:width 0.4s;"></div>'
        f'</div>'
        f'<span style="color:#555;font-size:0.72rem;font-weight:600;font-variant-numeric:tabular-nums;text-align:right;">{score:.1f}</span>'
        f'</div>'
    )


def render_stat_ab_test():
    """Statistical hypothesis testing: two-proportion z-test, t-test, sample size calculator."""
    try:
        import math
        import numpy as np
        from scipy import stats as sc
        from scipy.stats import norm as _norm
    except ImportError:
        st.warning("Install scipy to enable statistical testing: `pip install scipy`")
        return

    ALPHA = 0.05

    # ── shared render helpers ────────────────────────────────────────────────
    def _pfmt(p):
        return "< 0.001" if p < 0.001 else f"{p:.4f}"

    def _kv(lbl, val):
        return (
            f'<div style="display:flex;justify-content:space-between;padding:7px 0;'
            f'border-bottom:1px solid #111;">'
            f'<span style="color:#888;font-size:0.78rem;">{lbl}</span>'
            f'<span style="color:#D8D8D8;font-size:0.84rem;font-weight:600;'
            f'font-variant-numeric:tabular-nums;">{val}</span></div>'
        )

    def _verdict(sig, headline, body, ci_lbl=None, ci_val=None):
        c = GREEN if sig else AMBER
        tag = "SIGNIFICANT" if sig else "NOT SIGNIFICANT"
        html = (
            f'<div style="border:1px solid {c}28;border-left:3px solid {c};border-radius:7px;'
            f'padding:18px 20px;margin-top:14px;background:#0A0A0A;">'
            f'<div style="color:{c};font-size:0.62rem;font-weight:700;letter-spacing:0.14em;'
            f'text-transform:uppercase;margin-bottom:8px;">{tag}</div>'
            f'<div style="color:#E0E0E0;font-size:0.9rem;font-weight:600;margin-bottom:8px;">{headline}</div>'
            f'<p style="color:#A8A8A8;font-size:0.84rem;line-height:1.75;margin:0;">{body}</p>'
        )
        if ci_lbl:
            html += (
                f'<div style="margin-top:12px;padding-top:12px;border-top:1px solid #181818;">'
                f'<span style="color:#FF6B3B;font-size:0.62rem;font-weight:700;letter-spacing:0.1em;">'
                f'{ci_lbl}</span>'
                f'<span style="color:#CCC;font-size:0.84rem;margin-left:10px;">{ci_val}</span>'
                f'</div>'
            )
        html += '</div>'
        return html

    # ════════════════════════════════════════════════════════════════════════
    # 1. Two-proportion z-test
    # ════════════════════════════════════════════════════════════════════════
    _eyebrow("Two-Proportion Z-Test")
    st.markdown(
        '<p style="color:#A0A0A0;font-size:0.84rem;margin:0 0 20px;">'
        'Compare click-through rates between a control and up to four variants. '
        'For 3 or more variants, Bonferroni correction is applied automatically '
        'to control the family-wise error rate.</p>',
        unsafe_allow_html=True,
    )

    n_var  = st.radio("Total variants (including control)", [2, 3, 4, 5], horizontal=True, key="z_nv")
    VLBLS  = ["Control (A)", "Variant B", "Variant C", "Variant D", "Variant E"]
    VCLRS  = [ACCENT, "#6366F1", GREEN, AMBER, RED]

    z_ps, z_ns = [], []
    for i in range(n_var):
        ca, cb = st.columns(2, gap="large")
        with ca:
            st.markdown(
                f'<span style="color:{VCLRS[i]};font-size:0.65rem;font-weight:700;'
                f'letter-spacing:0.1em;">{VLBLS[i].upper()} — CTR (%)</span>',
                unsafe_allow_html=True,
            )
            p_i = st.number_input(
                f"CTR {VLBLS[i]}", min_value=0.001, max_value=100.0,
                value=round(2.5 + i * 0.4, 3), step=0.001, format="%.3f",
                key=f"z_p_{i}", label_visibility="collapsed",
            )
            z_ps.append(p_i / 100)
        with cb:
            st.markdown(
                f'<span style="color:{VCLRS[i]};font-size:0.65rem;font-weight:700;'
                f'letter-spacing:0.1em;">{VLBLS[i].upper()} — IMPRESSIONS</span>',
                unsafe_allow_html=True,
            )
            n_i = st.number_input(
                f"N {VLBLS[i]}", min_value=100, value=10000, step=100,
                key=f"z_n_{i}", label_visibility="collapsed",
            )
            z_ns.append(n_i)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("Run Z-Tests", type="primary", key="btn_ztest"):
        n_comps   = n_var - 1
        alpha_adj = ALPHA / n_comps if n_comps > 1 else ALPHA

        if n_comps > 1:
            st.markdown(
                f'<div style="background:#0D0D0D;border:1px solid #1E1E1E;border-radius:6px;'
                f'padding:10px 16px;margin-bottom:16px;display:flex;align-items:center;gap:12px;">'
                f'<span style="color:#FF6B3B;font-size:0.62rem;font-weight:700;letter-spacing:0.1em;">'
                f'BONFERRONI</span>'
                f'<span style="color:#A0A0A0;font-size:0.82rem;">'
                f'{n_comps} comparisons → adjusted alpha: {ALPHA} / {n_comps} = '
                f'<strong style="color:#E0E0E0;">{alpha_adj:.4f}</strong></span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        ctrl_p, ctrl_n = z_ps[0], z_ns[0]
        for i in range(1, n_var):
            vp, vn    = z_ps[i], z_ns[i]
            c_conv    = round(ctrl_p * ctrl_n)
            v_conv    = round(vp * vn)
            if c_conv < 5 or v_conv < 5:
                st.warning(
                    f"{VLBLS[i]}: fewer than 5 conversions in a group — z-test unreliable. "
                    "Increase impressions or CTR."
                )
                continue
            try:
                z_stat, p_val = sc.proportions_ztest(
                    [c_conv, v_conv], [ctrl_n, vn], alternative="two-sided"
                )
                diff = vp - ctrl_p
                se_u = math.sqrt(ctrl_p*(1-ctrl_p)/ctrl_n + vp*(1-vp)/vn)
                ci   = (diff - 1.96*se_u, diff + 1.96*se_u)
                rel  = diff / ctrl_p * 100 if ctrl_p else 0
                sig  = p_val <= alpha_adj
                dirn = "higher" if vp > ctrl_p else "lower"

                st.markdown(
                    f'<div style="border:1px solid #1A1A1A;border-radius:7px;padding:14px 18px;'
                    f'margin-top:14px;background:#0A0A0A;">'
                    f'<div style="color:#A0A0A0;font-size:0.72rem;font-weight:600;margin-bottom:10px;">'
                    f'Control vs {VLBLS[i]}</div>'
                    + _kv("Z-Statistic", f"{z_stat:+.4f}")
                    + _kv("P-Value", _pfmt(p_val))
                    + _kv("Alpha" + (" (Bonferroni-adjusted)" if n_comps > 1 else ""), f"{alpha_adj:.4f}")
                    + _kv("Relative lift", f"{rel:+.2f}%")
                    + _kv("95% CI (absolute difference)", f"[{ci[0]*100:+.3f}%, {ci[1]*100:+.3f}%]")
                    + '</div>',
                    unsafe_allow_html=True,
                )
                if sig:
                    body = (
                        f"Variant {VLBLS[i].split()[-1]} CTR ({vp*100:.3f}%) is {abs(rel):.1f}% {dirn} "
                        f"than control ({ctrl_p*100:.3f}%) and is statistically significant at the "
                        f"adjusted threshold of {alpha_adj:.4f} (p = {_pfmt(p_val)}). "
                        f"The 95% CI does not cross zero, confirming the effect is real."
                    )
                else:
                    body = (
                        f"The observed {abs(rel):.1f}% {'lift' if rel > 0 else 'drop'} "
                        f"(control {ctrl_p*100:.3f}% vs variant {vp*100:.3f}%) is not statistically "
                        f"significant (p = {_pfmt(p_val)}, threshold = {alpha_adj:.4f}). "
                        f"The 95% CI crosses zero. Run the test longer or increase the sample size "
                        f"before drawing conclusions."
                    )
                head = f"{'Reject H₀' if sig else 'Fail to reject H₀'} — {VLBLS[i]}"
                st.markdown(_verdict(sig, head, body), unsafe_allow_html=True)
            except Exception as exc:
                st.error(f"Z-test failed for {VLBLS[i]}: {exc}")

    # ════════════════════════════════════════════════════════════════════════
    # 2. Independent t-test (continuous metrics)
    # ════════════════════════════════════════════════════════════════════════
    _sep()
    _eyebrow("Independent T-Test (Continuous Metrics)")
    st.markdown(
        '<p style="color:#A0A0A0;font-size:0.84rem;margin:0 0 20px;">'
        "Compare means for continuous metrics such as ROAS, revenue per user, or AOV. "
        "Paste comma-separated values for each group. "
        "Welch’s t-test is used, so equal variances are not assumed.</p>",
        unsafe_allow_html=True,
    )
    tc1, tc2 = st.columns(2, gap="large")
    with tc1:
        st.markdown(
            f'<span style="color:{ACCENT};font-size:0.65rem;font-weight:700;letter-spacing:0.1em;">'
            f'CONTROL VALUES</span>', unsafe_allow_html=True,
        )
        ctrl_raw = st.text_area(
            "Control", value="2.1, 3.5, 1.8, 2.9, 2.4, 3.1, 1.9, 2.7",
            height=90, key="t_ctrl", label_visibility="collapsed",
            placeholder="e.g. 2.1, 3.5, 1.8, 2.9",
        )
    with tc2:
        st.markdown(
            '<span style="color:#6366F1;font-size:0.65rem;font-weight:700;letter-spacing:0.1em;">'
            'VARIANT VALUES</span>', unsafe_allow_html=True,
        )
        var_raw = st.text_area(
            "Variant", value="3.2, 4.1, 2.8, 3.9, 3.5, 4.3, 2.9, 3.7",
            height=90, key="t_var", label_visibility="collapsed",
            placeholder="e.g. 3.2, 4.1, 2.8, 3.9",
        )
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("Run T-Test", type="primary", key="btn_ttest"):
        try:
            def _parse(s):
                return [float(x) for x in re.split(r"[\s,;]+", s.strip()) if x]
            a, b = np.array(_parse(ctrl_raw)), np.array(_parse(var_raw))
            if len(a) < 2 or len(b) < 2:
                st.error("Each group needs at least 2 values.")
            else:
                t_stat, p_val = sc.ttest_ind(a, b, equal_var=False)
                m1, m2 = float(a.mean()), float(b.mean())
                s1, s2 = float(a.std(ddof=1)), float(b.std(ddof=1))
                n1, n2 = len(a), len(b)
                df_ws  = (s1**2/n1 + s2**2/n2)**2 / (
                    (s1**2/n1)**2/(n1-1) + (s2**2/n2)**2/(n2-1)
                )
                se_d   = math.sqrt(s1**2/n1 + s2**2/n2)
                t_crit = sc.t.ppf(0.975, df=df_ws)
                diff_m = m2 - m1
                ci_m   = (diff_m - t_crit*se_d, diff_m + t_crit*se_d)
                sig    = p_val <= ALPHA
                rel    = diff_m / m1 * 100 if m1 else 0
                dirn   = "higher" if m2 > m1 else "lower"

                st.markdown(
                    f'<div style="border:1px solid #1A1A1A;border-radius:7px;padding:14px 18px;'
                    f'margin-top:14px;background:#0A0A0A;">'
                    f'<div style="color:#A0A0A0;font-size:0.72rem;font-weight:600;margin-bottom:10px;">'
                    f"Welch’s Independent T-Test</div>"
                    + _kv("T-Statistic", f"{t_stat:+.4f}")
                    + _kv("P-Value (two-tailed)", _pfmt(p_val))
                    + _kv("Degrees of Freedom (Welch-Satterthwaite)", f"{df_ws:.1f}")
                    + _kv("Control: n / mean / SD", f"{n1} / {m1:.4f} / {s1:.4f}")
                    + _kv("Variant: n / mean / SD", f"{n2} / {m2:.4f} / {s2:.4f}")
                    + _kv("95% CI (mean difference)", f"[{ci_m[0]:+.4f}, {ci_m[1]:+.4f}]")
                    + '</div>',
                    unsafe_allow_html=True,
                )
                if sig:
                    body = (
                        f"The variant mean ({m2:.4f}) is {abs(rel):.1f}% {dirn} than the control "
                        f"mean ({m1:.4f}). This difference is statistically significant "
                        f"(p = {_pfmt(p_val)}, df = {df_ws:.1f}). "
                        f"The 95% CI [{ci_m[0]:+.4f}, {ci_m[1]:+.4f}] does not cross zero."
                    )
                else:
                    body = (
                        f"The observed difference (control {m1:.4f} vs variant {m2:.4f}, {rel:+.1f}%) "
                        f"is not statistically significant (p = {_pfmt(p_val)}). "
                        f"With n={n1} and n={n2}, there is insufficient evidence to conclude the "
                        f"variant outperforms the control. Collect more observations before deciding."
                    )
                head = f"{'Reject H₀' if sig else 'Fail to reject H₀'} — mean diff {diff_m:+.4f}"
                st.markdown(
                    _verdict(sig, head, body,
                             ci_lbl="95% CI FOR MEAN DIFFERENCE",
                             ci_val=f"[{ci_m[0]:+.4f}, {ci_m[1]:+.4f}]"),
                    unsafe_allow_html=True,
                )
        except (ValueError, ZeroDivisionError) as exc:
            st.error(f"Parse error: ensure all values are numeric. ({exc})")

    # ════════════════════════════════════════════════════════════════════════
    # 3. Sample size calculator
    # ════════════════════════════════════════════════════════════════════════
    _sep()
    _eyebrow("Sample Size Calculator")
    st.markdown(
        '<p style="color:#A0A0A0;font-size:0.84rem;margin:0 0 20px;">'
        'Calculate the minimum observations per variant to detect a given effect with sufficient '
        'power. Based on the two-proportion z-test power formula (Fleiss, 1981).</p>',
        unsafe_allow_html=True,
    )
    sc1, sc2, sc3, sc4 = st.columns(4, gap="large")
    with sc1:
        base_pct = st.number_input("Baseline CTR (%)", min_value=0.01, max_value=99.0, value=2.5, step=0.01, format="%.2f", key="ss_base")
    with sc2:
        mde_pct = st.number_input(
            "Min. Detectable Effect (%)", min_value=1.0, max_value=200.0, value=10.0,
            step=0.5, format="%.1f", key="ss_mde",
            help="Relative lift to detect. 10 means detect a 10% relative improvement in CTR.",
        )
    with sc3:
        pow_v = st.slider("Power (1 − β)", min_value=0.70, max_value=0.99, value=0.80, step=0.01, key="ss_pow", format="%.2f")
    with sc4:
        alp_v = st.slider("Alpha (α)", min_value=0.01, max_value=0.20, value=0.05, step=0.005, key="ss_alp", format="%.3f")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("Calculate Sample Size", type="primary", key="btn_ss"):
        p1    = base_pct / 100
        p2    = min(p1 * (1 + mde_pct / 100), 0.9999)
        z_a   = _norm.ppf(1 - alp_v / 2)
        z_b   = _norm.ppf(pow_v)
        p_avg = (p1 + p2) / 2
        n_f   = (
            (z_a * math.sqrt(2 * p_avg * (1 - p_avg)) + z_b * math.sqrt(p1*(1-p1) + p2*(1-p2)))
            / abs(p2 - p1)
        ) ** 2
        n_per   = math.ceil(n_f)
        n_total = n_per * 2

        st.markdown(
            f'<div style="border:1px solid #1A1A1A;border-radius:7px;padding:14px 18px;'
            f'margin-top:14px;background:#0A0A0A;">'
            + _kv("Baseline CTR", f"{p1*100:.2f}%")
            + _kv("Variant CTR (baseline + MDE)", f"{p2*100:.4f}%")
            + _kv("Absolute difference", f"{(p2-p1)*100:.4f} pp")
            + _kv("Statistical power", f"{pow_v:.0%}")
            + _kv("Significance level (α)", f"{alp_v:.3f}")
            + _kv("Required n per variant", f"{n_per:,}")
            + _kv("Total n (both variants)", f"{n_total:,}")
            + '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="border:1px solid {ACCENT}28;border-left:3px solid {ACCENT};'
            f'border-radius:7px;padding:20px 24px;margin-top:14px;background:#0A0A0A;">'
            f'<div style="color:#FF6B3B;font-size:0.62rem;font-weight:700;letter-spacing:0.14em;'
            f'text-transform:uppercase;margin-bottom:10px;">Result</div>'
            f'<div style="color:#EDEDED;font-size:2rem;font-weight:700;font-variant-numeric:tabular-nums;'
            f'letter-spacing:-0.03em;line-height:1;margin-bottom:10px;">{n_per:,}'
            f'<span style="font-size:0.9rem;color:#888;font-weight:400;margin-left:8px;">per variant</span></div>'
            f'<p style="color:#A8A8A8;font-size:0.84rem;line-height:1.75;margin:0;">'
            f'To detect a {mde_pct:.0f}% relative lift in CTR (from {p1*100:.2f}% to {p2*100:.4f}%) '
            f'with {pow_v:.0%} power at α = {alp_v:.3f}, you need at least '
            f'<strong style="color:#E0E0E0;">{n_per:,} observations per variant</strong> '
            f'({n_total:,} total). Running the experiment with fewer observations risks a Type II '
            f'error: failing to detect a real effect and potentially shipping an inferior variant.'
            f'</p></div>',
            unsafe_allow_html=True,
        )


def render_ab_scorer_tab():
    # ── Statistical A/B Test ─────────────────────────────────────────────────
    render_stat_ab_test()

    _sep()

    # ── Copy Quality Scorer (NLP) ────────────────────────────────────────────
    _eyebrow("Copy Quality Scorer")
    st.markdown(
        '<p style="color:#A0A0A0;font-size:0.84rem;margin:0 0 20px;">'
        'Rule-based NLP analysis across four dimensions: Clarity, Relevance, Urgency, and CTA '
        'Strength. Enter headline and body copy for each variant to get a weighted score out of 10.</p>',
        unsafe_allow_html=True,
    )

    # Scoring criteria cards
    criteria = [
        ("💡", "Clarity", "30%", "Headline length, body structure, readability"),
        ("🎯", "Relevance", "30%", "Power words, specificity, benefit language"),
        ("⏱", "Urgency", "20%", "Time pressure, action triggers, numbers"),
        ("📣", "CTA Strength", "20%", "Action verbs, direct calls to action"),
    ]
    crit_cols = st.columns(4, gap="medium")
    for col, (icon, dim, wt, desc) in zip(crit_cols, criteria):
        col.markdown(
            f'<div style="border:1px solid #141414;border-radius:7px;padding:16px 14px;'
            f'transition:border-color 0.15s;cursor:default;" '
            f'onmouseover="this.style.borderColor=\'#FF6B3B44\'" '
            f'onmouseout="this.style.borderColor=\'#141414\'">'
            f'<div style="font-size:1.1rem;margin-bottom:9px;">{icon}</div>'
            f'<div style="color:#B8B8B8;font-size:0.84rem;font-weight:600;margin-bottom:3px;">{dim}</div>'
            f'<div style="color:{ACCENT};font-size:0.67rem;font-weight:700;letter-spacing:0.06em;margin-bottom:6px;">{wt} weight</div>'
            f'<div style="color:#A0A0A0;font-size:0.72rem;line-height:1.5;">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    _sep()
    _eyebrow("Variant Inputs")

    col_n, _ = st.columns([1, 4])
    with col_n:
        n = st.slider("Variants", min_value=2, max_value=5, value=2)

    inputs = []
    VARIANT_COLORS = [ACCENT, "#6366F1", GREEN, AMBER, RED]

    for i in range(n):
        lbl = chr(65 + i)
        vc = VARIANT_COLORS[i % len(VARIANT_COLORS)]

        if i > 0:
            st.markdown('<div style="border-top:1px solid #0F0F0F;margin:20px 0 16px;"></div>', unsafe_allow_html=True)

        # Variant label row
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">'
            f'<div style="width:26px;height:26px;border-radius:5px;background:{vc}18;'
            f'border:1px solid {vc}30;display:flex;align-items:center;justify-content:center;flex-shrink:0;">'
            f'<span style="color:{vc};font-size:0.7rem;font-weight:700;">{lbl}</span></div>'
            f'<span style="color:#AAAAAA;font-size:0.8rem;font-weight:500;">Variant {lbl}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns([1, 1.4], gap="large")
        with c1:
            hl = st.text_input(
                "Headline",
                key=f"hl{i}",
                placeholder="e.g., Save 3 Hours Daily with AI",
            )
            hl_len = len(st.session_state.get(f"hl{i}", ""))
            hl_pct = min(hl_len / 40, 1.0)
            hl_c = (GREEN if 1 <= hl_len <= 40 else RED if hl_len > 40 else "#181818")
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:8px;margin-top:-6px;margin-bottom:4px;">'
                f'<div style="flex:1;height:2px;background:#111;border-radius:1px;overflow:hidden;">'
                f'<div style="height:100%;width:{hl_pct*100:.0f}%;background:{hl_c};'
                f'border-radius:1px;transition:width 0.15s,background 0.15s;"></div></div>'
                f'<span style="color:{hl_c};font-size:0.66rem;font-variant-numeric:tabular-nums;'
                f'white-space:nowrap;min-width:32px;text-align:right;">{hl_len}/40</span></div>',
                unsafe_allow_html=True,
            )
        with c2:
            bd = st.text_area(
                "Ad Body",
                key=f"bd{i}",
                placeholder="e.g., Join 10,000 teams who automate their workflow. Start free today.",
                height=88,
            )
            bd_raw = st.session_state.get(f"bd{i}", "")
            bd_words = len(bd_raw.split()) if bd_raw.strip() else 0
            bd_c = (GREEN if bd_words >= 8 else AMBER if bd_words >= 3 else "#181818")
            st.markdown(
                f'<span style="color:{bd_c};font-size:0.66rem;margin-top:-6px;'
                f'display:block;font-variant-numeric:tabular-nums;">{bd_words} words</span>',
                unsafe_allow_html=True,
            )

        inputs.append({"name": f"Variant {lbl}", "headline": hl, "body": bd})

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    if not st.button("Score All Variants", type="primary", use_container_width=True):
        return

    valid = [v for v in inputs if v["headline"] and v["body"]]
    if len(valid) < 2:
        st.error("Enter at least 2 complete variants.")
        return

    rows = []
    for v in valid:
        cl = _score_clarity(v["headline"], v["body"])
        ur = _score_urgency(v["headline"], v["body"])
        rv = _score_relevance(v["headline"], v["body"])
        ct = _score_cta(v["headline"], v["body"])
        ov = _overall(cl, ur, rv, ct)
        rows.append({"name": v["name"], "cl": cl, "ur": ur, "rv": rv, "ct": ct, "ov": ov})

    rows.sort(key=lambda r: r["ov"], reverse=True)

    _sep()
    _eyebrow("Ranked Results")

    dim_colors = {"cl": "#6366F1", "ur": RED, "rv": GREEN, "ct": AMBER}
    dim_labels = {"cl": "Clarity", "ur": "Urgency", "rv": "Relevance", "ct": "CTA Strength"}

    for rank, row in enumerate(rows):
        ov = row["ov"]
        ov_color = GREEN if ov >= 7.5 else (AMBER if ov >= 5.5 else RED)
        is_winner = rank == 0

        bars_html = "".join(_score_bar_html(dim_labels[k], row[k], dim_colors[k]) for k in ["cl", "rv", "ur", "ct"])

        border_style = f"border:1px solid rgba(255,107,59,0.15);border-left:3px solid #FF6B3B;" if is_winner else "border:1px solid #141414;"

        st.markdown(
            f'<div style="{border_style}border-radius:7px;padding:22px 24px;margin-bottom:10px;'
            f'background:{"#0D0D0D" if is_winner else "#0A0A0A"};">'

            f'<div style="display:flex;align-items:baseline;justify-content:space-between;margin-bottom:18px;">'
            f'<div style="display:flex;align-items:baseline;gap:14px;">'
            f'<span style="color:#888;font-size:0.72rem;font-weight:700;font-variant-numeric:tabular-nums;">#{rank+1}</span>'
            f'<span style="color:{"#E8E8E8" if is_winner else "#666"};font-size:0.875rem;font-weight:{"600" if is_winner else "400"};">{row["name"]}</span>'
            + (f'<span style="color:#FF6B3B;font-size:0.67rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;">RECOMMENDED</span>' if is_winner else '')
            + f'</div>'
            f'<span style="color:{ov_color};font-size:1.3rem;font-weight:700;font-variant-numeric:tabular-nums;letter-spacing:-0.02em;">{ov:.1f}<span style="font-size:0.75rem;color:#888;font-weight:500;">/10</span></span>'
            f'</div>'

            f'{bars_html}'

            f'</div>',
            unsafe_allow_html=True,
        )

    # Charts
    _sep()
    _eyebrow("Visual Breakdown")

    bar_col, radar_col = st.columns(2, gap="large")

    with bar_col:
        fig_bar = go.Figure()
        dl = {"cl": "Clarity", "rv": "Relevance", "ur": "Urgency", "ct": "CTA Strength", "ov": "Overall"}
        dc = {"cl": "#6366F1", "rv": GREEN, "ur": RED, "ct": AMBER, "ov": ACCENT}
        for k, lbl in dl.items():
            fig_bar.add_trace(go.Bar(
                name=lbl, x=[r["name"] for r in rows], y=[r[k] for r in rows],
                marker_color=dc[k], text=[f"{r[k]:.1f}" for r in rows],
                textposition="outside", textfont=dict(size=10, color="#444", family="Inter"),
            ))
        fig_bar.update_layout(
            barmode="group", height=300,
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(color="#777", gridcolor="#111", tickfont=dict(size=11, family="Inter")),
            yaxis=dict(range=[0, 12], color="#666", gridcolor="#111",
                       tickfont=dict(size=10, family="Inter")),
            legend=dict(font=dict(size=10, color="#888", family="Inter"), bgcolor="rgba(0,0,0,0)",
                        orientation="h", y=1.08, x=0),
            margin=dict(l=0, r=0, t=30, b=0), font=dict(family="Inter"),
            title=dict(text="Score by Dimension", font=dict(size=11, color="#888", family="Inter"), x=0),
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    with radar_col:
        dims = ["Clarity", "Urgency", "Relevance", "CTA Strength"]
        radar_c = [(ACCENT, "rgba(255,107,59,0.12)"), ("#6366F1","rgba(99,102,241,0.12)"),
                   (GREEN,"rgba(34,197,94,0.12)"), (AMBER,"rgba(245,158,11,0.12)"), (RED,"rgba(239,68,68,0.12)")]
        fig_r = go.Figure()
        for i, row in enumerate(rows):
            lc, fc = radar_c[i % len(radar_c)]
            vals = [row[k] for k in ["cl", "ur", "rv", "ct"]] + [row["cl"]]
            fig_r.add_trace(go.Scatterpolar(
                r=vals, theta=dims + [dims[0]], fill="toself", name=row["name"],
                line=dict(color=lc, width=1.5), fillcolor=fc,
            ))
        fig_r.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0, 10], color="#444",
                                gridcolor="#1A1A1A", tickfont=dict(size=8, family="Inter", color="#666")),
                angularaxis=dict(color="#555", gridcolor="#1A1A1A",
                                 tickfont=dict(size=10, family="Inter", color="#888")),
            ),
            showlegend=True,
            legend=dict(font=dict(size=10, color="#888", family="Inter"), bgcolor="rgba(0,0,0,0)"),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            height=300, margin=dict(l=10, r=10, t=30, b=10), font=dict(family="Inter"),
            title=dict(text="Radar Comparison", font=dict(size=11, color="#888", family="Inter"), x=0.5),
        )
        st.plotly_chart(fig_r, use_container_width=True, config={"displayModeBar": False})

    # Recommendation prose
    _sep()
    winner = rows[0]
    runner = rows[1] if len(rows) > 1 else None
    best_dim_key = max(["cl", "ur", "rv", "ct"], key=lambda k: winner[k])
    best_dim_name = dim_labels[best_dim_key]
    gap = winner["ov"] - runner["ov"] if runner else 0

    rec = (
        f"{winner['name']} is your strongest performer at {winner['ov']:.1f}/10, "
        f"leading on {best_dim_name} ({winner[best_dim_key]:.1f}/10). "
    )
    if runner:
        rec += (
            f"Launch it as your primary creative. {runner['name']} ({runner['ov']:.1f}/10) is close "
            f"and worth testing as a challenger."
            if gap < 0.7 else
            f"It outscores {runner['name']} by {gap:.1f} points. Use {winner['name']} as your primary creative."
        )

    st.markdown(
        f'<div style="border:1px solid #141414;border-radius:7px;padding:22px 24px;">'
        f'<div style="color:#FF6B3B;font-size:0.64rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:10px;">Recommendation</div>'
        f'<p style="color:#A8A8A8;font-size:0.9rem;line-height:1.75;margin:0;">{rec}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    inject_css()

    with st.sidebar:
        api_ok = get_anthropic_client() is not None
        dot_c = GREEN if api_ok else AMBER
        status_lbl = "Connected" if api_ok else "Not configured"

        st.markdown(
            f'<div style="margin-bottom:24px;">'
            f'<div style="color:#D8D8D8;font-size:0.9rem;font-weight:700;letter-spacing:-0.01em;margin-bottom:2px;">Marketing AI</div>'
            f'<div style="color:#999;font-size:0.72rem;">Automation Platform</div>'
            f'</div>'

            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:28px;padding-bottom:20px;border-bottom:1px solid #101010;">'
            f'<div style="width:7px;height:7px;border-radius:50%;background:{dot_c};flex-shrink:0;'
            f'box-shadow:0 0 5px {dot_c}44;"></div>'
            f'<span style="color:#C0C0C0;font-size:0.78rem;font-weight:500;">{status_lbl}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        if not api_ok:
            st.markdown(
                '<div style="background:#0C0C0C;border:1px solid #141414;border-radius:6px;padding:12px 14px;margin-bottom:20px;">'
                '<p style="color:#A0A0A0;font-size:0.75rem;line-height:1.7;margin:0;">'
                'Add <code style="font-size:0.72rem;color:#CCC;background:#1A1A1A;padding:1px 4px;border-radius:3px;">ANTHROPIC_API_KEY</code> '
                'to Streamlit secrets. All tabs work in fallback mode without it.'
                '</p></div>',
                unsafe_allow_html=True,
            )

        sidebar_info = [
            ("Model", "claude-haiku-4-5"),
            ("Fallback", "Template + Rule engine"),
            ("Charts", "Plotly"),
            ("Tabs", "3"),
        ]
        for label, val in sidebar_info:
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #0E0E0E;">'
                f'<span style="color:#888;font-size:0.75rem;">{label}</span>'
                f'<span style="color:#D0D0D0;font-size:0.75rem;font-weight:500;">{val}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            '<div style="margin-top:28px;">'
            '<div style="color:#999;font-size:0.72rem;font-weight:600;margin-bottom:4px;">Ridhan Parvendhan</div>'
            '<div style="color:#666;font-size:0.68rem;line-height:1.6;">All sample data is synthetic and for demonstration only.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    # Page header
    st.markdown(
        '<div style="margin-bottom:32px;">'
        '<h1 style="color:#EDEDED;font-size:1.6rem;font-weight:700;letter-spacing:-0.025em;margin:0 0 4px;">Marketing AI Platform</h1>'
        '<p style="color:#A0A0A0;font-size:0.875rem;margin:0;">Ad copy generation, campaign analytics, and variant scoring.</p>'
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
