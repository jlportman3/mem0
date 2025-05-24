# System Patterns

Mem0 uses a dual storage design composed of a vector database for memories and a graph database for relationships. LLMs extract key information from conversations, and memories are retrieved using semantic search with optional graph queries. The main API exposes `add` and `search` operations.

The repository includes a Python package, a REST API server using FastAPI, and optional UI under OpenMemory. Docker is used for local development with Memgraph as the graph database.
