import json

def load_trades(path="data/trades.json"):
    with open(path, "r") as f:
        return json.load(f)

def score_trade(profile, trade):
    profile_skills = [s.lower() for s in profile["existing_skills"] + profile["interests"]]
    trade_skills = [s.lower() for s in trade["skills"]]

    matched = set()
    for t_skill in trade_skills:
        for p_skill in profile_skills:
            # match if either phrase contains the other
            if t_skill in p_skill or p_skill in t_skill:
                matched.add(t_skill)
                break

    score = len(matched)

    if profile["employment_preference"] == trade["employment_type"] or trade["employment_type"] == "both":
        score += 1

    return score, matched

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