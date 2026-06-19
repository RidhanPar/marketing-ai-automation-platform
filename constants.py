BENCHMARK_THRESHOLDS = {
    "CTR (%)": {"good": 1.5, "warn": 0.8, "higher_is_better": True},
    "CPC ($)": {"good": 1.5, "warn": 2.5, "higher_is_better": False},
    "CPM ($)": {"good": 4.0, "warn": 8.0, "higher_is_better": False},
    "ROAS": {"good": 3.0, "warn": 1.5, "higher_is_better": True},
    "Conversion Rate (%)": {"good": 3.0, "warn": 1.5, "higher_is_better": True},
}

INDUSTRY_BENCHMARKS = {
    "CTR (%)": 1.0,
    "CPC ($)": 2.0,
    "CPM ($)": 5.0,
    "ROAS": 2.0,
    "Conversion Rate (%)": 2.5,
}

POWER_WORDS = [
    "free", "save", "proven", "guaranteed", "exclusive", "limited",
    "instant", "easy", "powerful", "trusted", "results", "transform",
    "boost", "grow", "unlock", "achieve", "discover", "new", "best",
    "top", "leading", "award", "certified", "expert", "premium",
]

CTA_KEYWORDS = [
    "buy now", "shop now", "learn more", "sign up", "get started",
    "try free", "download", "subscribe", "contact us", "book now",
    "claim", "register", "apply now", "start today", "see how",
    "get yours", "order now", "request", "explore", "join now",
]

URGENCY_WORDS = [
    "now", "today", "limited", "hurry", "last chance", "expires",
    "deadline", "urgent", "immediately", "fast", "quick", "instant",
    "only", "exclusive", "never miss", "act fast", "ends soon",
    "while supplies", "time sensitive", "don't wait", "final",
]

CLARITY_POSITIVE = [
    "simple", "easy", "straightforward", "clear", "effortless",
    "seamless", "intuitive", "no hassle", "just", "simply",
    "step by step", "in minutes", "no experience", "beginner",
]

TEMPLATE_AD_COPY = {
    "Awareness": [
        {
            "headline": "Meet {product}",
            "primary_text": "Discover how {product} helps {audience} with {usp}. Join thousands already seeing results.",
            "cta": "Learn More",
            "rationale": "Brand introduction with a soft {tone} tone is ideal for top-of-funnel {objective} campaigns that prioritize reach over immediate conversion.",
        },
        {
            "headline": "{product}: The Trusted Choice",
            "primary_text": "Built for {audience}, {product} delivers {usp}. See why leading teams trust us.",
            "cta": "Discover More",
            "rationale": "Social proof drives {objective} recall. A {tone} credential statement builds credibility before the audience actively searches for solutions.",
        },
        {
            "headline": "Introducing {product}",
            "primary_text": "{product} gives {audience} the power to achieve {usp}. Experience the difference today.",
            "cta": "See How It Works",
            "rationale": "Product-centric messaging for {objective} establishes a clear value proposition in a {tone} voice, anchoring the brand in memory.",
        },
    ],
    "Traffic": [
        {
            "headline": "{product}: See It In Action",
            "primary_text": "Click to see how {product} helps {audience} achieve {usp}. Explore features and success stories.",
            "cta": "Explore Now",
            "rationale": "Action-oriented copy for {objective} drives clicks by inviting exploration. The {tone} message focuses on curiosity rather than pressure.",
        },
        {
            "headline": "Why {product} Stands Out",
            "primary_text": "{audience} uses {product} to achieve {usp}. Browse demos, reviews, and real results.",
            "cta": "Browse Now",
            "rationale": "Evidence-based copy for {objective} invites site visits with a {tone} appeal to comparison shoppers who want proof before deciding.",
        },
        {
            "headline": "Compare Your Options",
            "primary_text": "Find out how {product} delivers {usp} for {audience}. Side-by-side comparisons available.",
            "cta": "Compare Options",
            "rationale": "Comparative positioning for {objective} attracts in-market buyers. A {tone} tone respects the audience's research process.",
        },
    ],
    "Conversions": [
        {
            "headline": "Get Results Starting Today",
            "primary_text": "{product} helps {audience} achieve {usp} fast. Special pricing available for a limited time.",
            "cta": "Get Started",
            "rationale": "Urgency-driven copy with a clear benefit for {objective} works best. The {tone} voice creates forward momentum without overpromising.",
        },
        {
            "headline": "Join {product} Members",
            "primary_text": "Thousands of {audience} already achieve {usp} with {product}. Limited spots available this week.",
            "cta": "Claim Your Spot",
            "rationale": "Scarcity combined with social proof for {objective} drives immediate action. The {tone} tone makes the offer feel credible, not pushy.",
        },
        {
            "headline": "Try {product} Risk-Free",
            "primary_text": "{product} delivers {usp} for {audience}. No commitment required. Cancel anytime.",
            "cta": "Start Free Trial",
            "rationale": "Risk-reversal messaging for {objective} reduces purchase anxiety. A {tone} approach keeps the ask low while still driving a conversion event.",
        },
    ],
    "Leads": [
        {
            "headline": "Free Resource: {usp}",
            "primary_text": "Download our exclusive guide for {audience} and learn how {product} can help. No email spam, ever.",
            "cta": "Download Free",
            "rationale": "A lead magnet with a clear promise works for {objective} by exchanging value for contact info. The {tone} tone builds trust before the pitch.",
        },
        {
            "headline": "Does {product} Fit You?",
            "primary_text": "Designed for {audience} who want {usp}. Answer 3 quick questions to see your personalized plan.",
            "cta": "Check Eligibility",
            "rationale": "Qualification copy for {objective} creates micro-commitment and filters quality leads. The {tone} voice feels helpful rather than salesy.",
        },
        {
            "headline": "Book a Free {product} Demo",
            "primary_text": "See how {product} delivers {usp} for {audience}. 20-minute call, no obligation.",
            "cta": "Book Free Demo",
            "rationale": "A low-friction demo offer for {objective} reduces barriers. The {tone} approach signals respect for the prospect's time.",
        },
    ],
}
