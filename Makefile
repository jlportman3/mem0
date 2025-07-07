.PHONY: pull build rebuild start stop clean

DOCKER_IMAGE_NAME = universal-llm-api

pull:
	docker pull qdrant/qdrant
	docker pull memgraph/memgraph-mage

build:
	cp -r jmemory universal_api/jmemory
	cd universal_api && docker build -t $(DOCKER_IMAGE_NAME) .
	rm -rf universal_api/jmemory

rebuild:
	cp -r jmemory universal_api/jmemory
	cd universal_api && docker build --no-cache -t $(DOCKER_IMAGE_NAME) .
	rm -rf universal_api/jmemory

start:
	docker-compose up -d

stop:
	docker-compose down

clean:
	docker-compose down -v --rmi all
