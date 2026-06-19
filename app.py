import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import re
import os

st.set_page_config(
    page_title="Marketing AI Automation Platform",
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


# ---------------------------------------------------------------------------
# TAB 1 - Ad Copy Generator
# ---------------------------------------------------------------------------

OBJECTIVE_COLORS = {
    "Awareness": "#4A90D9",
    "Traffic": "#27AE60",
    "Conversions": "#F39C12",
    "Leads": "#9B59B6",
}


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
        data = json.loads(match.group())
        return data[:3]
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
        prod_short = product[:18]
        usp_short = usp[:20]
        headline = tmpl["headline"].format(
            product=prod_short, modifier=mod, usp=usp_short
        )[:40]
        primary_text = tmpl["primary_text"].format(
            product=product, audience=audience, usp=usp, modifier=mod
        )[:125]
        cta = tmpl["cta"]
        rationale = tmpl["rationale"].format(objective=objective, tone=tone)
        variants.append(
            {
                "headline": headline,
                "primary_text": primary_text,
                "cta": cta,
                "rationale": rationale,
            }
        )
    return variants


def render_ad_copy_tab():
    st.header("Ad Copy Generator")
    st.markdown(
        "Generate three high-converting ad variants tailored to your campaign objective and tone."
    )

    col_l, col_r = st.columns(2)
    with col_l:
        product = st.text_input(
            "Product / Service Name", placeholder="e.g., CloudSync Pro"
        )
        audience = st.text_input(
            "Target Audience",
            placeholder="e.g., Small business owners aged 25 to 45",
        )
        usp = st.text_input(
            "Key Selling Point",
            placeholder="e.g., Saves 5 hours per week",
        )
    with col_r:
        objective = st.selectbox(
            "Campaign Objective", ["Awareness", "Traffic", "Conversions", "Leads"]
        )
        tone = st.selectbox(
            "Tone", ["Professional", "Casual", "Urgent", "Inspirational"]
        )

    if st.button("Generate Ad Copy", type="primary", use_container_width=True):
        if not product or not audience or not usp:
            st.error("Please fill in all three text fields before generating.")
            return

        with st.spinner("Crafting your ad variants..."):
            client = get_anthropic_client()
            variants = None
            used_ai = False
            if client:
                try:
                    variants = _call_ai_for_ad_copy(
                        client, product, audience, objective, tone, usp
                    )
                    used_ai = True
                except Exception as exc:
                    st.warning(
                        f"AI generation unavailable ({str(exc)[:60]}). Using template engine."
                    )
            if not variants:
                variants = _template_ad_copy(product, audience, objective, tone, usp)

        if used_ai:
            st.success("Generated with Anthropic claude-haiku-4-5")
        else:
            st.info("Generated with template engine (add ANTHROPIC_API_KEY to enable AI)")

        color = OBJECTIVE_COLORS.get(objective, "#4A90D9")
        labels = ["Variant A", "Variant B", "Variant C"]

        for i, v in enumerate(variants):
            st.markdown(f"### {labels[i]}")
            c1, c2, c3 = st.columns([5, 5, 2])

            with c1:
                hl = v.get("headline", "")
                hlen = len(hl)
                hcolor = "#27AE60" if hlen <= 40 else "#E74C3C"
                st.markdown(
                    f"**Headline** "
                    f"<span style='color:{hcolor};font-size:0.85em'>({hlen}/40 chars)</span>",
                    unsafe_allow_html=True,
                )
                st.code(hl, language=None)

            with c2:
                pt = v.get("primary_text", "")
                ptlen = len(pt)
                ptcolor = "#27AE60" if ptlen <= 125 else "#E74C3C"
                st.markdown(
                    f"**Primary Text** "
                    f"<span style='color:{ptcolor};font-size:0.85em'>({ptlen}/125 chars)</span>",
                    unsafe_allow_html=True,
                )
                st.code(pt, language=None)

            with c3:
                cta = v.get("cta", "Learn More")
                st.markdown("**CTA Button**")
                st.markdown(
                    f"<div style='background:{color};color:#fff;padding:10px 14px;"
                    f"border-radius:6px;text-align:center;font-weight:700;"
                    f"margin-top:6px;font-size:0.9em'>{cta}</div>",
                    unsafe_allow_html=True,
                )

            rationale = v.get("rationale", "")
            st.markdown(
                f"> **Why this works for {objective}:** {rationale}"
            )
            st.divider()


# ---------------------------------------------------------------------------
# TAB 2 - Campaign Performance Analyzer
# ---------------------------------------------------------------------------

GREEN = "#27AE60"
AMBER = "#F39C12"
RED = "#E74C3C"


def _metric_color(col_name, value):
    cfg = BENCHMARK_THRESHOLDS.get(col_name)
    if cfg is None:
        return ""
    good, warn, higher = cfg["good"], cfg["warn"], cfg["higher_is_better"]
    if higher:
        bg = GREEN if value >= good else (AMBER if value >= warn else RED)
    else:
        bg = GREEN if value <= good else (AMBER if value <= warn else RED)
    return f"background-color:{bg};color:#fff;font-weight:600"


def _style_row(row):
    styles = []
    for col in row.index:
        if col in BENCHMARK_THRESHOLDS:
            try:
                raw = str(row[col]).replace("%", "").replace("$", "").replace(",", "").strip()
                val = float(raw)
                styles.append(_metric_color(col, val))
            except (ValueError, TypeError):
                styles.append("")
        else:
            styles.append("")
    return styles


def _analyze_with_ai(client, df_str):
    prompt = (
        "You are a senior digital marketing analyst. Analyze this campaign performance data:\n\n"
        f"{df_str}\n\n"
        "Industry benchmarks: CTR > 1% is good, ROAS > 2x is profitable, CPC < $2 is efficient, CPM < $5 is efficient.\n\n"
        "Provide a structured analysis with these three sections:\n"
        "1. What is Working Well (2 to 3 specific bullet points with numbers from the data)\n"
        "2. What is Underperforming (2 to 3 specific bullet points with numbers)\n"
        "3. Three Actionable Recommendations (numbered, each with an expected outcome)\n\n"
        "Be concrete. Reference specific campaigns and metrics. No em dashes."
    )
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=900,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def _analyze_with_rules(df):
    good_points, bad_points, recs = [], [], []

    for _, row in df.iterrows():
        name = row.get("Campaign", "This campaign")

        for col, higher, threshold_good, threshold_warn, unit, fmt in [
            ("CTR (%)", True, 1.5, 0.8, "%", "{:.2f}"),
            ("ROAS", True, 3.0, 1.5, "x", "{:.1f}"),
            ("CPC ($)", False, 1.5, 2.5, "", "${:.2f}"),
            ("CPM ($)", False, 4.0, 8.0, "", "${:.2f}"),
        ]:
            if col not in df.columns:
                continue
            try:
                val = float(str(row[col]).replace("$", "").replace("%", "").replace("x", "").replace(",", ""))
            except (ValueError, TypeError):
                continue

            formatted = fmt.format(val) + unit if not fmt.startswith("$") else "${:.2f}".format(val)
            if higher:
                if val >= threshold_good:
                    good_points.append(f"{name} achieves a strong {col} of {formatted} (benchmark: good above {threshold_good}{unit})")
                elif val < threshold_warn:
                    bad_points.append(f"{name} {col} of {formatted} falls below the {threshold_warn}{unit} benchmark")
                    if col == "CTR (%)":
                        recs.append(f"Test new creative angles for {name} to lift CTR above 1%")
                    elif col == "ROAS":
                        recs.append(f"Review bidding and audience quality for {name} to push ROAS above 2x")
            else:
                if val <= threshold_good:
                    good_points.append(f"{name} keeps {col} efficient at {formatted} (target: below ${threshold_good:.2f})")
                elif val > threshold_warn:
                    bad_points.append(f"{name} {col} of {formatted} exceeds the ${threshold_warn:.2f} target")
                    if col == "CPC ($)":
                        recs.append(f"Tighten audience targeting for {name} to reduce CPC toward $1.50")
                    elif col == "CPM ($)":
                        recs.append(f"Broaden reach targeting for {name} to lower CPM below $5")

    if not good_points:
        good_points = [
            "All campaigns are generating impressions and driving measurable traffic",
            "Ad spend is being distributed across multiple campaigns, reducing single-point risk",
        ]
    if not bad_points:
        bad_points = [
            "Performance is within expected ranges with room for incremental optimization",
            "Minor efficiency gaps exist that targeted bid adjustments can address",
        ]

    default_recs = [
        "A/B test headline variants across all campaigns to identify a 15 to 20% CTR lift",
        "Implement dayparting to concentrate budget on hours with the highest conversion rate",
        "Build lookalike audiences from your top 10% converters to improve ROAS across all campaigns",
    ]
    final_recs = (recs + default_recs)[:3]

    lines = ["**What is Working Well**"]
    for p in good_points[:3]:
        lines.append(f"- {p}")
    lines.append("")
    lines.append("**What is Underperforming**")
    for p in bad_points[:3]:
        lines.append(f"- {p}")
    lines.append("")
    lines.append("**Three Actionable Recommendations**")
    for idx, r in enumerate(final_recs, 1):
        lines.append(f"{idx}. {r}")
    return "\n".join(lines)


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


def render_performance_tab():
    st.header("Campaign Performance Analyzer")
    st.markdown(
        "Upload or enter campaign metrics to see color-coded benchmarks and AI-generated insights."
    )

    b1, b2, b3, b4 = st.columns(4)
    b1.metric("CTR Benchmark", "> 1.0%", help="Click-through rate industry baseline")
    b2.metric("ROAS Benchmark", "> 2.0x", help="Minimum return on ad spend for profitability")
    b3.metric("CPC Target", "< $2.00", help="Cost per click efficiency target")
    b4.metric("CPM Target", "< $5.00", help="Cost per thousand impressions target")

    st.divider()

    method = st.radio("Data input method", ["Manual Entry", "Upload CSV"], horizontal=True)
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
            st.info(
                "Expected columns: Campaign, Impressions, Clicks, Conversions, "
                "Spend ($), Reach, CTR (%), CPC ($), CPM ($), ROAS"
            )

    if df is not None and not df.empty:
        st.markdown("### Color-Coded Performance Overview")
        legend_html = (
            "<span style='background:#27AE60;color:#fff;padding:3px 10px;border-radius:4px;margin-right:6px'>Strong</span>"
            "<span style='background:#F39C12;color:#fff;padding:3px 10px;border-radius:4px;margin-right:6px'>Needs Attention</span>"
            "<span style='background:#E74C3C;color:#fff;padding:3px 10px;border-radius:4px'>Underperforming</span>"
        )
        st.markdown(legend_html, unsafe_allow_html=True)
        st.markdown("")

        try:
            styled = df.style.apply(_style_row, axis=1)
            st.dataframe(styled, use_container_width=True)
        except Exception:
            st.dataframe(df, use_container_width=True)

        st.markdown("### Aggregate KPIs")
        agg_cols = st.columns(5)
        kpi_defs = [
            ("Avg CTR", "CTR (%)", lambda v: f"{v:.2f}%"),
            ("Avg CPC", "CPC ($)", lambda v: f"${v:.2f}"),
            ("Avg CPM", "CPM ($)", lambda v: f"${v:.2f}"),
            ("Avg ROAS", "ROAS", lambda v: f"{v:.2f}x"),
            ("Total Conversions", "Conversions", lambda v: f"{v:,.0f}"),
        ]
        for col_widget, (label, col_name, fmt_fn) in zip(agg_cols, kpi_defs):
            if col_name in df.columns:
                try:
                    nums = pd.to_numeric(
                        df[col_name].astype(str).str.replace(r"[$%x,]", "", regex=True),
                        errors="coerce",
                    )
                    val = nums.sum() if "Total" in label else nums.mean()
                    col_widget.metric(label, fmt_fn(val))
                except Exception:
                    pass

        st.markdown("### AI Performance Analysis")
        if st.button("Analyze Campaigns", type="primary"):
            with st.spinner("Analyzing performance data..."):
                client = get_anthropic_client()
                df_str = df.to_string(index=False)
                if client:
                    try:
                        analysis = _analyze_with_ai(client, df_str)
                        st.success("Analysis powered by Anthropic claude-haiku-4-5")
                    except Exception as exc:
                        st.warning(
                            f"AI unavailable ({str(exc)[:60]}). Showing rule-based analysis."
                        )
                        analysis = _analyze_with_rules(df)
                else:
                    analysis = _analyze_with_rules(df)
                    st.info("Rule-based analysis active (add ANTHROPIC_API_KEY to enable AI)")
                st.markdown(analysis)


# ---------------------------------------------------------------------------
# TAB 3 - A/B Variant Scorer
# ---------------------------------------------------------------------------


def _score_clarity(headline, body):
    score = 5.0
    words_h = len(headline.split())
    if 4 <= words_h <= 8:
        score += 2.0
    elif words_h < 3 or words_h > 12:
        score -= 1.0
    words_b = len(body.split())
    if 15 <= words_b <= 35:
        score += 2.0
    elif words_b < 5:
        score -= 2.0
    elif words_b > 55:
        score -= 1.0
    body_lower = body.lower()
    hits = sum(1 for w in CLARITY_POSITIVE if w in body_lower)
    score += min(hits * 0.5, 1.5)
    if "?" in headline:
        score -= 0.5
    return min(max(round(score, 1), 0.0), 10.0)


def _score_urgency(headline, body):
    score = 3.0
    combined = (headline + " " + body).lower()
    hits = sum(1 for w in URGENCY_WORDS if w in combined)
    score += min(hits * 1.2, 5.0)
    score += min(combined.count("!") * 0.5, 1.5)
    if re.search(r"\d+", combined):
        score += 0.5
    return min(max(round(score, 1), 0.0), 10.0)


def _score_relevance(headline, body):
    score = 4.0
    combined = (headline + " " + body).lower()
    power_hits = sum(1 for w in POWER_WORDS if w in combined)
    score += min(power_hits * 0.6, 3.0)
    if re.search(r"\d+%|\d+x|\$\d+|\d+ hours|\d+ days|\d+ minutes", combined):
        score += 1.5
    benefit_words = ["save", "get", "increase", "reduce", "improve", "boost", "gain", "earn"]
    benefit_hits = sum(1 for w in benefit_words if w in combined)
    score += min(benefit_hits * 0.5, 1.5)
    return min(max(round(score, 1), 0.0), 10.0)


def _score_cta(headline, body):
    score = 3.0
    combined = (headline + " " + body).lower()
    cta_hits = sum(1 for kw in CTA_KEYWORDS if kw in combined)
    score += min(cta_hits * 1.5, 5.0)
    action_verbs = ["start", "join", "discover", "unlock", "claim", "try", "get", "book", "download"]
    action_hits = sum(1 for w in action_verbs if w in combined)
    score += min(action_hits * 0.5, 1.5)
    if "you" in combined or "your" in combined:
        score += 0.5
    return min(max(round(score, 1), 0.0), 10.0)


def _overall(clarity, urgency, relevance, cta):
    return round(clarity * 0.30 + urgency * 0.20 + relevance * 0.30 + cta * 0.20, 1)


def render_ab_scorer_tab():
    st.header("A/B Variant Scorer")
    st.markdown(
        "Score and rank your ad copy variants across four dimensions using rule-based NLP analysis."
    )

    st.markdown(
        "**Scoring weights:** Clarity 30% | Relevance 30% | Urgency 20% | CTA Strength 20%"
    )

    num_variants = st.slider("Number of variants", min_value=2, max_value=5, value=2)
    variants_input = []

    for i in range(num_variants):
        label = chr(65 + i)
        with st.expander(f"Variant {label}", expanded=(i < 2)):
            c1, c2 = st.columns(2)
            with c1:
                hl = st.text_input(
                    f"Headline (Variant {label})",
                    key=f"ab_hl_{i}",
                    placeholder="e.g., Save 3 Hours Daily with AI",
                )
            with c2:
                bd = st.text_area(
                    f"Ad Body (Variant {label})",
                    key=f"ab_bd_{i}",
                    placeholder="e.g., Join 10,000 teams who automate their workflow. Start free today.",
                    height=80,
                )
        variants_input.append({"name": f"Variant {label}", "headline": hl, "body": bd})

    if st.button("Score All Variants", type="primary", use_container_width=True):
        valid = [v for v in variants_input if v["headline"] and v["body"]]
        if len(valid) < 2:
            st.error("Please enter at least 2 complete variants (headline and body text).")
            return

        rows = []
        for v in valid:
            cl = _score_clarity(v["headline"], v["body"])
            ur = _score_urgency(v["headline"], v["body"])
            re_ = _score_relevance(v["headline"], v["body"])
            ct = _score_cta(v["headline"], v["body"])
            ov = _overall(cl, ur, re_, ct)
            rows.append(
                {
                    "Variant": v["name"],
                    "Clarity": cl,
                    "Urgency": ur,
                    "Relevance": re_,
                    "CTA Strength": ct,
                    "Overall Score": ov,
                }
            )

        results = pd.DataFrame(rows).sort_values("Overall Score", ascending=False).reset_index(drop=True)

        st.markdown("### Score Table")

        def _cell_color(val):
            if not isinstance(val, (int, float)):
                return ""
            if val >= 7.0:
                return f"background-color:{GREEN};color:#fff"
            if val >= 5.0:
                return f"background-color:{AMBER};color:#fff"
            return f"background-color:{RED};color:#fff"

        score_cols = ["Clarity", "Urgency", "Relevance", "CTA Strength", "Overall Score"]
        try:
            styled_results = results.style.map(_cell_color, subset=score_cols)
            st.dataframe(styled_results, use_container_width=True, hide_index=True)
        except AttributeError:
            # pandas < 2.1 fallback
            styled_results = results.style.applymap(_cell_color, subset=score_cols)
            st.dataframe(styled_results, use_container_width=True, hide_index=True)

        st.markdown("### Ranked Bar Chart")
        dim_colors = {
            "Clarity": "#4A90D9",
            "Urgency": "#E74C3C",
            "Relevance": "#27AE60",
            "CTA Strength": "#9B59B6",
            "Overall Score": "#F39C12",
        }
        fig = go.Figure()
        for dim in ["Clarity", "Urgency", "Relevance", "CTA Strength", "Overall Score"]:
            fig.add_trace(
                go.Bar(
                    name=dim,
                    x=results["Variant"].tolist(),
                    y=results[dim].tolist(),
                    marker_color=dim_colors[dim],
                    text=[f"{v:.1f}" for v in results[dim].tolist()],
                    textposition="outside",
                )
            )
        fig.update_layout(
            barmode="group",
            title="Ad Copy Variant Scores by Dimension",
            xaxis_title="Variant",
            yaxis_title="Score (0 to 10)",
            yaxis=dict(range=[0, 12]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FAFAFA"),
            height=460,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Recommendation")
        winner = results.iloc[0]
        runner = results.iloc[1] if len(results) > 1 else None
        best_dim = max(
            ["Clarity", "Urgency", "Relevance", "CTA Strength"],
            key=lambda d: winner[d],
        )
        rec = (
            f"**Test {winner['Variant']} first** with an overall score of {winner['Overall Score']:.1f}/10. "
            f"It leads on {best_dim} ({winner[best_dim]:.1f}/10)"
        )
        if runner is not None:
            gap = winner["Overall Score"] - runner["Overall Score"]
            if gap < 0.5:
                rec += (
                    f", though {runner['Variant']} ({runner['Overall Score']:.1f}/10) "
                    f"is close enough to include as a direct A/B challenger."
                )
            else:
                rec += f" and outscores {runner['Variant']} by {gap:.1f} points."
        st.info(rec)

        st.markdown("### Per-Variant Dimension Breakdown")
        metric_cols = st.columns(len(valid))
        for col_widget, (_, row) in zip(metric_cols, results.iterrows()):
            col_widget.markdown(f"**{row['Variant']}**")
            col_widget.metric("Clarity", f"{row['Clarity']}/10")
            col_widget.metric("Urgency", f"{row['Urgency']}/10")
            col_widget.metric("Relevance", f"{row['Relevance']}/10")
            col_widget.metric("CTA Strength", f"{row['CTA Strength']}/10")
            col_widget.metric("Overall", f"{row['Overall Score']}/10")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    st.title("Marketing AI Automation Platform")
    st.markdown(
        "*Intelligent tools for ad creation, performance analysis, and variant scoring*"
    )

    with st.sidebar:
        st.markdown("### API Status")
        client = get_anthropic_client()
        if client:
            st.success("Anthropic API: Connected")
        else:
            st.warning("Anthropic API: Not configured")
            st.caption(
                "Add `ANTHROPIC_API_KEY` to `.streamlit/secrets.toml` or your "
                "environment variables to enable AI features. All tabs work without it."
            )
        st.divider()
        st.markdown("**Author:** Ridhan Parvendhan")
        st.caption(
            "All sample data shown in this app is synthetic and for demonstration purposes only."
        )

    tab1, tab2, tab3 = st.tabs(
        ["Ad Copy Generator", "Campaign Performance Analyzer", "A/B Variant Scorer"]
    )
    with tab1:
        render_ad_copy_tab()
    with tab2:
        render_performance_tab()
    with tab3:
        render_ab_scorer_tab()


if __name__ == "__main__":
    main()
