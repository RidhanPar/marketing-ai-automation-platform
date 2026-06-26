"""Tests for the offline fallbacks in ``app.py``.

When no Anthropic API key is configured the app must still produce useful
output: a rule-based campaign analysis (``_analyze_with_rules``) and a
template-driven ad-copy generator (``_template_ad_copy``). These run with no
network access, so they are fully unit-testable.
"""
import re

import pandas as pd
import pytest


@pytest.fixture(scope="module")
def s(app_module):
    return app_module


@pytest.fixture
def mixed_campaigns():
    """One clearly strong campaign and one clearly underperforming campaign."""
    return pd.DataFrame(
        {
            "Campaign": ["Winner", "Loser"],
            "CTR (%)": [2.0, 0.5],
            "ROAS": [4.0, 1.0],
            "CPC ($)": [1.0, 3.0],
            "CPM ($)": [3.0, 9.0],
        }
    )


def _count_recommendations(report: str) -> int:
    in_recs = False
    count = 0
    for line in report.splitlines():
        if line.startswith("### Three Actionable Recommendations"):
            in_recs = True
            continue
        if in_recs and re.match(r"^\d+\.\s", line):
            count += 1
    return count


def test_analysis_contains_all_three_sections(s, mixed_campaigns):
    report = s._analyze_with_rules(mixed_campaigns)
    assert "### What is Working Well" in report
    assert "### What is Underperforming" in report
    assert "### Three Actionable Recommendations" in report


def test_strong_campaign_flagged_as_working(s, mixed_campaigns):
    report = s._analyze_with_rules(mixed_campaigns)
    working = report.split("### What is Underperforming")[0]
    assert "Winner" in working


def test_weak_campaign_flagged_as_underperforming(s, mixed_campaigns):
    report = s._analyze_with_rules(mixed_campaigns)
    underperforming = report.split("### What is Underperforming")[1]
    assert "Loser" in underperforming


def test_exactly_three_recommendations(s, mixed_campaigns):
    report = s._analyze_with_rules(mixed_campaigns)
    assert _count_recommendations(report) == 3


def test_analysis_falls_back_with_no_benchmark_columns(s):
    """Missing metric columns must not crash — defaults fill the sections."""
    df = pd.DataFrame({"Campaign": ["Alpha"], "Impressions": [1000]})
    report = s._analyze_with_rules(df)
    assert "### What is Working Well" in report
    assert _count_recommendations(report) == 3


def test_template_ad_copy_returns_three_filled_variants(s):
    variants = s._template_ad_copy(
        product="CloudSync Pro",
        audience="small business owners",
        objective="Conversions",
        tone="Professional",
        usp="saves five hours a week",
    )
    assert len(variants) == 3
    for v in variants:
        assert set(v) == {"headline", "primary_text", "cta", "rationale"}
        # Every placeholder must be substituted.
        for field in ("headline", "primary_text", "rationale"):
            assert "{" not in v[field] and "}" not in v[field]


def test_template_ad_copy_respects_character_limits(s):
    variants = s._template_ad_copy(
        product="A Very Long Product Name That Exceeds Limits",
        audience="enterprise teams",
        objective="Leads",
        tone="Urgent",
        usp="an unusually long unique selling proposition that keeps going",
    )
    for v in variants:
        assert len(v["headline"]) <= 40
        assert len(v["primary_text"]) <= 125


def test_template_ad_copy_supports_every_objective(s):
    for objective in ("Awareness", "Traffic", "Conversions", "Leads"):
        variants = s._template_ad_copy("X", "Y", objective, "Casual", "Z")
        assert len(variants) == 3
