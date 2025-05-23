build:
        docker build -t mem0-api-server .

# Build Memgraph image used for graph memory examples
memgraph-image:
        docker pull memgraph/memgraph-mage:latest

run_local:
        docker run -p 8000:8000 -v $(shell pwd):/app mem0-api-server --env-file .env

.PHONY: build run_local memgraph-image
