from textblob import TextBlob

def analyze_sentiment(text):
    try:
        polarity = TextBlob(text).sentiment.polarity
    except Exception:
        polarity = 0.0

    if polarity > 0.05:
        return "Positive"
    elif polarity < -0.05:
        return "Negative"
    else:
        return "Neutral"

def determine_priority(text, sentiment):
    text_lower = text.lower()
    
    # High priority keywords (severe complaints, security, fees/hall tickets, medical issues)
    critical_keywords = [
        "harassment", "abuse", "ragging", "emergency", "suicide", "depression", 
        "medical", "accident", "fight", "bribe", "stolen", "leak", "fire"
    ]
    
    # Medium priority keywords (academic issues, fee queries, portals, hall tickets)
    medium_keywords = [
        "exam", "fee", "fees", "payment", "hall ticket", "admit card", "marks", 
        "result", "attendance", "portal", "login", "password", "library"
    ]
    
    # High logic
    if any(kw in text_lower for kw in critical_keywords) or sentiment == "Negative":
        return "high"
    # Medium logic
    elif any(kw in text_lower for kw in medium_keywords) or sentiment == "Neutral":
        return "medium"
    
    return "low"
