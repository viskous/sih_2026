import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
THRESHOLD = 0.65

def load_trades(path="data/trades.json"):
    with open(path, "r") as f:
        return json.load(f)

def score_trade(profile, trade):

    profile_skills = (
        profile["existing_skills"]
        + profile["interests"]
    )

    trade_skills = trade["skills"]

    profile_embeddings = model.encode(profile_skills)
    trade_embeddings = model.encode(trade_skills)

    similarities = model.similarity(
        profile_embeddings,
        trade_embeddings
    )

    matched = set()

    for trade_index, trade_skill in enumerate(trade_skills):

        for profile_index, profile_skill in enumerate(profile_skills):

            similarity = similarities[profile_index][trade_index]

            if similarity >= THRESHOLD:
                matched.add(trade_skill)
                break

    score = len(matched)

    if (
        profile["employment_preference"] == trade["employment_type"]
        or trade["employment_type"] == "both"
    ):
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