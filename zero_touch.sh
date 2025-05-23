#!/bin/bash
set -e

# Default configuration
OLLAMA_URL="${OLLAMA_URL:-http://10.0.60.38:11434}"
OLLAMA_MODEL="${OLLAMA_MODEL:-llama3.3:latest}"
OPENAI_API_KEY="${OPENAI_API_KEY:-dummy}"
MEMGRAPH_PASSWORD="${MEMGRAPH_PASSWORD:-mem0graph}"
NEXT_PUBLIC_API_URL="${NEXT_PUBLIC_API_URL:-http://localhost:8765}"
USER="${USER:-$(whoami)}"

# Ensure Docker is available
if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required but not installed." >&2
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose v2 is required." >&2
  exit 1
fi

# Write docker-compose file
cat > docker-compose.yml <<COMPOSE
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

  memgraph:
    image: memgraph/memgraph-mage:latest
    command: --schema-info-enabled=True
    ports:
      - "7687:7687"

  openmemory-mcp:
    image: mem0/openmemory-mcp:latest
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - qdrant
      - memgraph
    ports:
      - "8765:8765"

volumes:
  qdrant_data:
COMPOSE

echo "Starting backend services..."
docker compose up -d

# Start UI container
if docker ps -a --format '{{.Names}}' | grep -q '^mem0_ui$'; then
  docker rm -f mem0_ui >/dev/null
fi

docker run -d --name mem0_ui \
  -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL="${NEXT_PUBLIC_API_URL}" \
  -e NEXT_PUBLIC_USER_ID="${USER}" \
  mem0/openmemory-ui:latest >/dev/null

echo "Waiting for MCP server..."
until curl -s "http://localhost:8765/docs" >/dev/null; do
  sleep 2
done

echo "Configuring OpenMemory..."
cat <<JSON | curl -s -X POST http://localhost:8765/configure -H 'Content-Type: application/json' -d @-
{
  "vector_store": {
    "provider": "qdrant",
    "config": {
      "collection_name": "openmemory",
      "host": "qdrant",
      "port": 6333
    }
  },
  "graph_store": {
    "provider": "memgraph",
    "config": {
      "url": "bolt://memgraph:7687",
      "username": "memgraph",
      "password": "${MEMGRAPH_PASSWORD}"
    }
  },
  "llm": {
    "provider": "ollama",
    "config": {
      "model": "${OLLAMA_MODEL}",
      "temperature": 0,
      "max_tokens": 2000,
      "ollama_base_url": "${OLLAMA_URL}"
    }
  },
  "embedder": {
    "provider": "ollama",
    "config": {
      "model": "nomic-embed-text:latest",
      "ollama_base_url": "${OLLAMA_URL}"
    }
  }
}
JSON

echo "Zero touch setup complete."
echo "UI: http://localhost:3000"
echo "MCP server: http://localhost:8765"
