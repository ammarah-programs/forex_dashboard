import requests
import re

CLOUDFLARE_AI_URL = "https://divine-base-9ee9.ammarahgraphics03.workers.dev"

def _strip_html(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"<[^>]+>", "", text).strip()

def analyze_news(pair: str, news_items: list) -> dict:
        # REMOVE SYSTEM PLACEHOLDER MESSAGES
    news_items = [
        item for item in news_items
        if item.get("source") != "System"
    ]

    if not news_items or not isinstance(news_items, list):
        return {
            "summary": "No high-impact news from trusted sources.",
            "impact": "Neutral",
            "confidence": 50,
            "deep_view": (
                "There are currently no major macroeconomic or geopolitical "
                "events affecting this forex pair."
            )
        }

    formatted_news = []
    for item in news_items:
        source = item.get("source", "Unknown")
        text = item.get("text", "")
        if text:
            formatted_news.append(f"[{source}] {text}")

    combined_text = "\n".join(formatted_news)[:3500]

    payload = {
        "pair": pair,
        "instructions": (
            "Analyze ONLY the provided news.\n"
            "Return PURE TEXT. NO HTML. NO TAGS.\n\n"
            "Output JSON with:\n"
            "- summary (1–2 sentences, plain text)\n"
            "- impact (Bullish, Bearish, Mixed, Neutral)\n"
            "- confidence (0–100)\n"
            "- deep_view (plain text explanation)"
        ),
        "news_text": combined_text
    }

    try:
        r = requests.post(CLOUDFLARE_AI_URL, json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()
       

        summary = _strip_html(
            data.get("summary")
            or data.get("analysis")
            or "No clear summary returned."
        )

        deep_view = _strip_html(
            data.get("deep_view")
            or data.get("details")
            or summary
        )

        raw_impact = (data.get("impact") or "").lower()

        if "bull" in raw_impact:
            impact = "Bullish"
        elif "bear" in raw_impact:
            impact = "Bearish"
        elif "mix" in raw_impact:
            impact = "Mixed"
        else:
            impact = "Neutral"

                  
       

            score = 0
            score += sum(term in text_blob for term in bullish_terms)
            score -= sum(term in text_blob for term in bearish_terms)

            if score > 0:
                impact = "Bullish"
                confidence = max(confidence, 65)
            elif score < 0:
                impact = "Bearish"
                confidence = max(confidence, 65)
 

        confidence = int(data.get("confidence", 55))
        confidence = max(0, min(100, confidence))

        
        # ADD THIS
        if confidence < 40:
            impact = "Neutral"


        return {
            "summary": summary,
            "impact": impact,
            "confidence": confidence,
            "deep_view": deep_view
        }

    except Exception as e:
        return {
            "summary": "AI analysis unavailable.",
            "impact": "Neutral",
            "confidence": 50,
            "deep_view": f"Cloudflare AI error: {e}"
        }
def ask_dashboard_ai(question: str, all_news: list) -> str:
    """
    Lightweight Q&A assistant.
    Reads today's aggregated news and answers user questions.
    DOES NOT affect bias, price, or summaries.
    """

    if not question.strip():
        return "Ask a question about today's macro news or FX bias."

    if not all_news:
        return "No news available to analyze today."

    formatted = []
    for item in all_news:
        text = item.get("text", "")
        source = item.get("source", "")
        if text:
            formatted.append(f"[{source}] {text}")

    news_blob = "\n".join(formatted)[:3500]

    payload = {
    "pair": "DASHBOARD",
     "instructions": (
        "You are an FX market assistant.\n"
        "Answer the user's question using ONLY the provided news.\n"
        "DO NOT infer or change directional bias.\n"
        "If the news is indirect or not FX-relevant, explicitly state that a Neutral bias is appropriate.\n"
        "Explain reasoning based on real sources only.\n"
        "Do NOT speculate beyond the articles.\n"
        "Plain text only."
    ),




    "news_text": (
        news_blob
        + "\n\nUSER QUESTION:\n"
        + question
    )
}


    try:
        r = requests.post(CLOUDFLARE_AI_URL, json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()

        answer = (
            data.get("summary")
            or data.get("analysis")
            or data.get("deep_view")
            or "No clear answer returned."
        )


        return _strip_html(answer)

    except Exception as e:
        return f"AI unavailable: {e}"

