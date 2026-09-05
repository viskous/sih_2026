import json

def load_trades(path="data/trades.json"):
    with open(path, "r") as f:
        return json.load(f)

def score_trade(profile, trade):
    profile_skills = set(profile["existing_skills"] + profile["interests"])
    trade_skills = set(trade["skills"])

    overlap = profile_skills & trade_skills
    score = len(overlap)

    # boost if employment preference matches
    if profile["employment_preference"] == trade["employment_type"] or trade["employment_type"] == "both":
        score += 1

    return score, overlap

def recommend(profile, trades_path="data/trades.json", top_n=3):
    trades = load_trades(trades_path)
    results = []

    for trade in trades:
        score, overlap = score_trade(profile, trade)
        if score > 0:
            results.append({
                "trade": trade["name"],
                "nsqf_level": trade["nsqf_level"],
                "score": score,
                "matched_skills": list(overlap)
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]