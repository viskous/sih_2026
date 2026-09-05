from dialogue.extract_profile import extract_profile

sample_conversation = """
I studied till 10th class. At home, my mother does tailoring, and I've helped her 
with stitching clothes for a few years. I'm good with a sewing machine. I'd like 
to learn more about garment work and maybe start my own small shop someday, 
rather than working for someone else. I can travel around my area without any 
issues. I live in Ghaziabad.
"""

profile = extract_profile(sample_conversation)
print("Extracted profile:")
print(profile)