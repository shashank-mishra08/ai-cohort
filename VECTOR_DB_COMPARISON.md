# Day 8 — Vector DB comparison (Chroma vs Pinecone)

Short survey for the healthcare coverage chatbot project.

## Landscape (quick map)

| Database | Type | Typical use |
|----------|------|-------------|
| **Chroma** | Local / self-hosted, open source | Prototypes, courses, laptops, small apps |
| **Pinecone** | Managed cloud | Production SaaS, teams that want zero ops |
| **FAISS** | Library (not a full server DB) | Fast similarity search inside your own app |
| **Weaviate** | Self-hosted or cloud | Hybrid search + richer schema |
| **Milvus** | Self-hosted / cloud | Large-scale vector search |

**Managed vs self-hosted**

- **Managed (e.g. Pinecone):** vendor runs servers, scaling, backups; you pay with money/limits; less ops work.
- **Self-hosted (e.g. Chroma on your machine):** free and private on your disk; you own the machine and backups.

**Indexing (high level)**

- **HNSW:** graph-based approximate nearest neighbor — great recall/latency balance (Chroma uses HNSW-style indexes).
- **IVF:** inverted file / coarse quantisation — good for very large collections with different speed/accuracy trade-offs.

**How to choose**

- **Scale:** laptop demo → Chroma/FAISS; multi-tenant production → Pinecone/Milvus/Weaviate cloud.
- **Latency:** all can be fast; network hop to cloud vs local disk matters.
- **Budget:** Chroma free local; Pinecone free tier then paid.
- **Access control:** enterprise RBAC / VPC often needs managed enterprise tiers or your own API layer in front of the DB.

---

## Chroma vs Pinecone (mission table)

| Dimension | **Chroma** | **Pinecone** |
|-----------|------------|--------------|
| **Local vs cloud** | Local (persistent folder on your machine); also can run as a server | Cloud-managed (serverless indexes) |
| **Free-tier limitations** | Free/open source; limited by your laptop disk/RAM | Free tier with usage caps; need account; beyond free → paid |
| **Latency** | Very low for local queries (no internet hop) | Low, but includes network RTT to the cloud region |
| **Ease of setup** | `pip install chromadb` + a few lines of Python | Sign up, API key, create index (dashboard or SDK) |
| **Per-member access control** | Not built-in multi-tenant ACLs; you filter in app code (e.g. metadata `member_id`) or separate collections | Metadata filters + your app logic; enterprise plans add stronger org controls |
| **Per-plan access control** | Same pattern: store `plan_id` / `plan_type` in metadata and filter at query time | Same: metadata filters on upserted vectors; app enforces who can query what |
| **Enterprise deployment** | Self-host in your VPC/K8s; you own security patches and HA | Managed enterprise features (SSO, private networking, SLAs) on higher tiers |

---

## Choice for the rest of this project

**We choose Chroma** as the primary vector database for the rest of this program.

Chroma is free, runs entirely on the local machine with no signup, and only needs a short Python setup to create a persistent client and a `coverage_kb` collection. That matches a learning project where the goal is to understand embeddings and retrieval without cloud billing, rate limits, or extra accounts blocking progress. Pinecone is still useful to learn (free-tier account + empty serverless index) so we understand managed cloud trade-offs, but day-to-day development and later RAG steps will use Chroma because it is simplest, fully offline-capable, and good enough at our current scale (a few hundred knowledge-base chunks).

---

## Day 8 status in this repo

| Item | Status |
|------|--------|
| Local Chroma install | `pip install chromadb` |
| Persistent path | `./chroma_db/` |
| Collection name | `coverage_kb` |
| Setup script | `python3 setup_chroma.py` |
| Pinecone helper | `python3 setup_pinecone.py` (needs `PINECONE_API_KEY`) |
| Comparison + decision | this file |
