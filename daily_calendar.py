from datetime import datetime
from collections import defaultdict

# -----------------------------
# KEYWORD WEIGHTS (IMPACT)
# -----------------------------
IMPACT_KEYWORDS = {
    "interest rate": 3,
    "rate hike": 3,
    "rate cut": 3,
    "inflation": 3,
    "cpi": 3,
    "ppi": 3,
    "nfp": 3,
    "employment": 2,
    "jobs": 2,
    "gdp": 2,
    "pmi": 2,
    "retail sales": 2,
    "central bank": 3,
    "fed": 3,
    "ecb": 3,
    "boe": 3,
    "boj": 3,
    "rba": 3,
}

# -----------------------------
# CURRENCY KEYWORDS
# -----------------------------
CURRENCY_MAP = {
    "USD": ["usd", "dollar", "fed", "treasury", "us"],
    "EUR": ["eur", "euro", "ecb"],
    "GBP": ["gbp", "pound", "boe"],
    "JPY": ["jpy", "yen", "boj"],
    "AUD": ["aud", "australian", "rba"],
    "CAD": ["cad", "canadian", "boc"],
    "NZD": ["nzd", "new zealand", "rbnz"],
    "CHF": ["chf", "swiss", "snb"],
}

# -----------------------------
# PAIR PRIORITY ORDER
# -----------------------------
PAIR_PRIORITY = [
    ("EURUSD", ["EUR", "USD"]),
    ("GBPUSD", ["GBP", "USD"]),
    ("USDJPY", ["USD", "JPY"]),
    ("AUDUSD", ["AUD", "USD"]),
    ("USDCAD", ["USD", "CAD"]),
    ("USDCHF", ["USD", "CHF"]),
    ("NZDUSD", ["NZD", "USD"]),
]

# -----------------------------
# CORE LOGIC
# -----------------------------
def build_daily_calendar(news_items):
    currency_scores = defaultdict(int)
    pinned_news = []

    for item in news_items:
        text = item["text"].lower()
        impact = 0

        # impact score
        for k, w in IMPACT_KEYWORDS.items():
            if k in text:
                impact += w

        if impact == 0:
            continue

        # currency detection
        detected_currencies = []

        for ccy, keys in CURRENCY_MAP.items():
            if any(k in text for k in keys):
                detected_currencies.append(ccy)

        for ccy in detected_currencies:
            currency_scores[ccy] += impact
            pinned_news.append({
                "source": item["source"],
                "text": item["text"],
                "impact": impact,
                "currency": ccy
            })



    pinned_news = sorted(
        pinned_news,
        key=lambda x: x["impact"],
        reverse=True
    )[:5]

    dominant_currency = max(currency_scores, key=currency_scores.get) if currency_scores else None
    if not dominant_currency and pinned_news:
        dominant_currency = pinned_news[0]["currency"]


    focus_pair = None
    if dominant_currency:
        for pair, ccys in PAIR_PRIORITY:
            if dominant_currency in ccys:
                focus_pair = pair
                break
    def format_pair(pair):
        return f"{pair[:3]}/{pair[3:]}" if pair else None


    return {
        "date": datetime.utcnow().strftime("%A, %d %B %Y"),
        "dominant_currency": dominant_currency,
        "focus_pair": format_pair(focus_pair),
        "pinned_news": pinned_news
    }
