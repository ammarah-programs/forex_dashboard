def impact_to_score(impact):
    impact = impact.lower()
    if "bullish" in impact:
        return 75
    if "bearish" in impact:
        return 25
    return 50
