import json
from recommender.recommend import recommend

# load the sample profile
with open("data/sample_profile.json", "r") as f:
    profile = json.load(f)

# run the recommender
results = recommend(profile)

# print output nicely
print("Beneficiary profile:")
print(json.dumps(profile, indent=2))
print("\nTop recommended trades:")
for r in results:
    print(f"- {r['trade']} (NSQF {r['nsqf_level']}, score: {r['score']}, matched: {r['matched_skills']})")