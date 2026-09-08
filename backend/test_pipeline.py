from dialogue.extract_profile import extract_profile
from recommender.recommend import recommend

sample_conversation = """
I studied till 10th class. At home, my mother does tailoring, and I've helped her with stitching clothes for a few years. I'm good with a sewing machine. I'd like to learn more about garment work and maybe start my own small shop someday, rather than working for someone else. I can travel around my area without any issues. I live in Ghaziabad.
"""

# Step 1: conversation -> structured profile
profile = extract_profile(sample_conversation)
print("Extracted profile:")
print(profile)

# Step 2: profile -> recommendations
results = recommend(profile)
print("\nRecommended trades:")
for r in results:
    print(f"- {r['trade']} (NSQF {r['nsqf_level']}, score: {r['score']}, matched: {r['matched_skills']})")