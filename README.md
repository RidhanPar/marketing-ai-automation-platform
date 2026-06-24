# Marketing AI Automation Platform

A polished, production-quality Streamlit application that combines AI-powered ad creation, data-driven campaign analysis, and NLP-based variant scoring into one unified marketing toolkit.

**Author:** Ridhan Parvendhan

---

## What It Does

### Tab 1: Ad Copy Generator

Input your product details, target audience, campaign objective, and tone to instantly generate three complete ad copy variants. Each variant includes a headline (40-character limit), primary text (125-character limit), a CTA button, and a rationale explaining why it suits your chosen objective. Powered by the Anthropic claude-haiku-4-5 API with a realistic template-based fallback when no API key is configured.

### Tab 2: Campaign Performance Analyzer

Paste or upload your campaign metrics table (CTR, CPC, CPM, ROAS, Impressions, Clicks, Conversions, Spend, Reach). The app color-codes each value against industry benchmarks: green for strong performance, amber for metrics that need attention, and red for underperformers. An AI-generated analysis covers what is working, what is underperforming, and three specific actionable recommendations. A rule-based analysis engine activates when no API key is present.

### Tab 3: A/B Variant Scorer

Tab 3 contains two independent analysis tools.

**Statistical A/B Test** (powered by scipy) provides rigorous hypothesis testing for real campaign data:

- Two-proportion z-test: enter click-through rates and impression counts for a control and up to four variants. Returns the z-statistic, p-value, result (reject or fail to reject H0), and a 95% confidence interval for the absolute difference in proportions. When three or more variants are tested, Bonferroni correction is applied automatically and the adjusted alpha threshold is shown.
- Independent t-test: paste comma-separated values for continuous metrics such as ROAS or revenue per user. Runs Welch's t-test (no equal-variance assumption), reporting the t-statistic, p-value, Welch-Satterthwaite degrees of freedom, group means and standard deviations, and a 95% CI for the difference in means.
- Sample size calculator: given a baseline CTR, minimum detectable effect (relative lift percentage), target power, and significance level, computes the required observations per variant using the two-proportion z-test power formula (Fleiss, 1981). Shows the total sample requirement and a plain-English explanation of the result.

Every result includes a plain-English interpretation card explaining whether the difference is significant, what the confidence interval means, and what action to take next.

**Copy Quality Scorer** (rule-based NLP, no API key required): input 2 to 5 ad copy variants (headline plus body text) and receive dimension scores across Clarity, Urgency, Relevance, and CTA Strength. An interactive Plotly grouped bar chart and radar chart rank all variants visually. A recommendation card identifies which variant to test first and why.

---

## Screenshots

1. **Ad Copy Generator** displays three complete ad variants side-by-side with live character counters, color-coded compliance indicators for platform limits, and styled CTA button previews matched to the selected campaign objective.

2. **Campaign Performance Analyzer** shows a color-coded data table comparing each campaign row against industry benchmarks, followed by an aggregate metrics row with KPI cards and a structured AI analysis panel with specific, numbered recommendations.

3. **A/B Variant Scorer** has two sub-sections. The Statistical A/B Test shows z-test and t-test results with significance cards, Bonferroni correction banners, and the sample size calculator with a large result display. The Copy Quality Scorer presents a grouped Plotly bar chart and radar chart comparing variants across four NLP dimensions, plus a recommendation card identifying the top variant.

---

## How to Run Locally

### Prerequisites

- Python 3.9 or higher
- An Anthropic API key (optional; the app runs in fallback mode without one)

### Setup

```bash
git clone https://github.com/RidhanPar/marketing-ai-automation-platform.git
cd marketing-ai-automation-platform

pip install -r requirements.txt

mkdir -p .streamlit
echo 'ANTHROPIC_API_KEY = "your-key-here"' >> .streamlit/secrets.toml

streamlit run app.py
```

The app opens at `http://localhost:8501`.

### Without an API Key

All three tabs work without an API key. Tabs 1 and 2 activate realistic template-based and rule-based fallback engines that produce varied, useful output. Tab 3 uses pure rule-based NLP scoring with no external calls at all.

---

## Deployment to Streamlit Community Cloud

1. Fork this repository to your GitHub account.
2. Visit [share.streamlit.io](https://share.streamlit.io) and connect your GitHub account.
3. Select the repository and set the main file to `app.py`.
4. Add your `ANTHROPIC_API_KEY` in the Streamlit Cloud secrets panel under Settings then Secrets.
5. Click Deploy.

---

## Data Notice

All sample data pre-loaded in this application is synthetic and generated for demonstration purposes only. No real campaign data, user information, or proprietary metrics are used or stored anywhere in this project.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Charts | Plotly |
| Data | Pandas |
| AI (Tabs 1 and 2) | Anthropic claude-haiku-4-5 |
| Statistical Testing (Tab 3) | scipy (z-test, t-test, power analysis) |
| Copy Scoring (Tab 3) | Rule-based NLP with keyword matching |
| Stats Dependencies | scipy, statsmodels |
| Deployment | Streamlit Community Cloud |
