"""Tests for the rule-based A/B copy-scoring functions in ``app.py``.

Each scorer maps a (headline, body) pair to a 0-10 score along one dimension.
The scores are deterministic and bounded, which makes them straightforward to
pin down: we assert the output range, the documented weighting, and that copy
exhibiting the target signal scores above copy that lacks it.
"""
import pytest

# Strong vs weak example copy for each scoring dimension.
STRONG_CLARITY = ("Save Five Hours Every Week", "Our simple tool makes weekly reporting effortless so your team can focus on work that matters instead of spreadsheets")
WEAK_CLARITY = ("Synergize", "Now")

STRONG_URGENCY = ("Last Chance Today", "Hurry, this exclusive offer expires in 24 hours, act fast before it is gone!")
WEAK_URGENCY = ("A Reporting Tool", "It helps teams put together their reports")

STRONG_RELEVANCE = ("Boost Revenue 30%", "Proven results: save $500 and increase output by 3x with our trusted premium platform")
WEAK_RELEVANCE = ("Hello There", "We have a thing you might want to look at sometime")

STRONG_CTA = ("Get Started Today", "Sign up now and claim your free trial, you will love how easy it is")
WEAK_CTA = ("An Update", "Here is some information about the situation")


@pytest.fixture(scope="module")
def s(app_module):
    return app_module


@pytest.mark.parametrize(
    "func_name,strong,weak",
    [
        ("_score_clarity", STRONG_CLARITY, WEAK_CLARITY),
        ("_score_urgency", STRONG_URGENCY, WEAK_URGENCY),
        ("_score_relevance", STRONG_RELEVANCE, WEAK_RELEVANCE),
        ("_score_cta", STRONG_CTA, WEAK_CTA),
    ],
)
def test_scores_stay_within_zero_to_ten(s, func_name, strong, weak):
    func = getattr(s, func_name)
    for headline, body in (strong, weak):
        score = func(headline, body)
        assert 0.0 <= score <= 10.0


@pytest.mark.parametrize(
    "func_name,strong,weak",
    [
        ("_score_clarity", STRONG_CLARITY, WEAK_CLARITY),
        ("_score_urgency", STRONG_URGENCY, WEAK_URGENCY),
        ("_score_relevance", STRONG_RELEVANCE, WEAK_RELEVANCE),
        ("_score_cta", STRONG_CTA, WEAK_CTA),
    ],
)
def test_strong_copy_outscores_weak_copy(s, func_name, strong, weak):
    func = getattr(s, func_name)
    assert func(*strong) > func(*weak)


def test_scores_are_deterministic(s):
    assert s._score_urgency(*STRONG_URGENCY) == s._score_urgency(*STRONG_URGENCY)
    assert s._score_relevance(*STRONG_RELEVANCE) == s._score_relevance(*STRONG_RELEVANCE)


def test_neutral_copy_sits_at_dimension_baseline(s):
    # No urgency keywords, exclamation marks, or digits -> base score of 3.0.
    assert s._score_urgency("Product Overview", "A calm description of what it does") == 3.0


def test_overall_applies_documented_weights(s):
    # Weights: clarity .30, urgency .20, relevance .30, cta .20.
    assert s._overall(10, 10, 10, 10) == 10.0
    assert s._overall(0, 0, 0, 0) == 0.0
    assert s._overall(10, 0, 0, 0) == 3.0  # clarity-only -> 0.30 * 10
    assert s._overall(0, 0, 10, 0) == 3.0  # relevance-only -> 0.30 * 10
    assert s._overall(0, 10, 0, 10) == 4.0  # urgency + cta -> 0.20 * 10 * 2


def test_overall_matches_manual_weighting(s):
    cl, ur, rv, ct = 7.0, 5.0, 8.0, 6.0
    expected = round(cl * 0.30 + ur * 0.20 + rv * 0.30 + ct * 0.20, 1)
    assert s._overall(cl, ur, rv, ct) == expected


def test_metric_color_higher_is_better(s):
    # ROAS: higher is better; good=3.0, warn=1.5.
    assert "background-color" in s._metric_color("ROAS", 4.0)
    strong = s._metric_color("ROAS", 4.0)
    weak = s._metric_color("ROAS", 1.0)
    assert s.GREEN in strong
    assert s.RED in weak


def test_metric_color_lower_is_better(s):
    # CPC: lower is better; good=1.5, warn=2.5.
    assert s.GREEN in s._metric_color("CPC ($)", 1.0)
    assert s.RED in s._metric_color("CPC ($)", 3.0)


def test_metric_color_unknown_column_returns_empty(s):
    assert s._metric_color("NotABenchmark", 5.0) == ""
