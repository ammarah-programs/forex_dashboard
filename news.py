import streamlit as st
import requests
import xml.etree.ElementTree as ET
import re

PAIR_KEYWORDS = {
    "EURUSD": ["euro", "ecb", "europe"],
    "GBPUSD": ["pound", "boe", "uk"],
    "USDJPY": ["yen", "boj", "japan"],
    "AUDUSD": ["australian", "rba", "australia"]
}

# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def clean_html(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<.*?>", "", text)
    return " ".join(text.split())

def tag_text(source: str, text: str) -> str:
    if source == "Investing.com":
        return f"[MACRO][Investing.com] {text}"
    if source == "IBD":
        return f"[SENTIMENT][IBD] {text}"
    if source == "ForexFactory":
        return f"[EVENT][ForexFactory] {text}"
    return text

IMPORTANT_TERMS = [
    "cpi", "inflation", "rates", "rate hike", "rate cut",
    "fed", "ecb", "boe", "boj",
    "gdp", "pmi", "yields", "employment"
]

# --------------------------------------------------
# RSS SOURCES
# --------------------------------------------------
INVESTING_RSS = "https://www.investing.com/rss/news_25.rss"
FOREX_FACTORY_RSS = "https://www.forexfactory.com/rss/news"
IBD_RSS = "https://www.investors.com/feed/"

# --------------------------------------------------
# RSS FETCHER
# --------------------------------------------------
@st.cache_data(ttl=1800)
def fetch_rss(url: str, source_name: str, limit: int = 5):
    items = []

    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/rss+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()

        root = ET.fromstring(r.content)

        for item in root.findall(".//item")[:limit]:
            title = clean_html(item.findtext("title", ""))
            desc = clean_html(item.findtext("description", ""))

            text = f"{title} {desc}".strip()
            if not text:
                continue

            items.append({
                "source": source_name,
                "text": tag_text(source_name, text)
            })

    except Exception as e:
        print(f"{source_name} RSS error:", e)

    return items

# --------------------------------------------------
# MAIN COLLECTOR
# --------------------------------------------------
def collect_pair_news(pair: str, keywords: list, calendar_mode=False):

    news_items = []
    news_items += fetch_rss(INVESTING_RSS, "Investing.com", limit=6)
    news_items += fetch_rss(IBD_RSS, "IBD", limit=3)
    news_items += fetch_rss(FOREX_FACTORY_RSS, "ForexFactory", limit=2)

    filtered = []

    for item in news_items:
        text = item["text"].lower()

        pair_keywords = PAIR_KEYWORDS.get(pair, [])
        mentions_pair = any(k in text for k in pair_keywords)

        terms = IMPORTANT_TERMS + keywords
        mentions_macro = any(term in text for term in terms)

        # Accept macro news even if pair is not explicitly mentioned
        if mentions_macro:
            filtered.append(item)


    if not filtered:
        return [{
            "source": "System",
            "text": (
                f"[SYSTEM] No strong macro headlines detected for {pair} at this time. "
                "Market likely driven by technicals or sentiment."
            )
        }]

    return filtered[:6]

