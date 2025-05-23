# Mem0 REST API Server

Mem0 provides a REST API server (written using FastAPI). Users can perform all operations through REST endpoints. The API also includes OpenAPI documentation, accessible at `/docs` when the server is running.

## Features

- **Create memories:** Create memories based on messages for a user, agent, or run.
- **Retrieve memories:** Get all memories for a given user, agent, or run.
- **Search memories:** Search stored memories based on a query.
- **Update memories:** Update an existing memory.
- **Delete memories:** Delete a specific memory or all memories for a user, agent, or run.
- **Reset memories:** Reset all memories for a user, agent, or run.
- **OpenAPI Documentation:** Accessible via `/docs` endpoint.

## Running the server

Follow the instructions in the [docs](https://docs.mem0.ai/open-source/features/rest-api) to run the server.

## Development

The `Makefile` in this directory provides helper commands:

- `make build` - build the API server Docker image.
- `make run_local` - run the server container locally.
- `make memgraph-image` - pull the Memgraph image used when experimenting with graph memory.
