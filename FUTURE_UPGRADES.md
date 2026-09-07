# Future Upgrades

## 1. Semantic skill matching (recommender)
**Current limitation:** The recommender matches skills using substring text matching (e.g. "sewing machine" must appear literally within a phrase like "sewing machine operation"). This misses synonyms or differently-worded but semantically equivalent skills (e.g. "farming" vs "agriculture", "machine stitching" vs "tailoring").

**Planned fix:** Replace substring matching in `recommender/recommend.py` with semantic similarity using sentence embeddings (`sentence-transformers` library). Instead of exact/substring text checks, compare the meaning of skill phrases using cosine similarity between embeddings. This would make matching robust to paraphrasing and vocabulary differences between how beneficiaries describe their skills and how trades are labeled in the dataset.

**Why deferred:** Current substring approach works correctly at MVP scale (small trades dataset, short skill phrases) and required zero additional dependencies or model downloads. Semantic matching adds a new dependency and slightly more complexity, better suited for a post-hackathon iteration once the core pipeline is proven.

---
## 2. Database (SQLite → PostgreSQL)
**Current:** SQLite is used for storing beneficiary profiles and recommendations — a single file, zero setup, sufficient for prototype/demo scale.

**Planned fix:** Migrate to PostgreSQL for production deployment, to support concurrent access (multiple beneficiaries/admins simultaneously), better performance at scale, and proper cloud hosting compatibility.

**Why deferred:** SQLite requires no server setup and is fully sufficient for a single-user demo and small-scale testing. PostgreSQL adds setup complexity (connection config, hosting) not worth taking on before the core logic is proven.