
import asyncio
import concurrent
import gc
import hashlib
import json
import logging
import os
import uuid
import warnings
from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Optional

import pytz
from pydantic import ValidationError

from jmemory.configs.base import MemoryConfig, MemoryItem
from jmemory.configs.enums import MemoryType
from jmemory.configs.prompts import (PROCEDURAL_MEMORY_SYSTEM_PROMPT,
                                  get_update_memory_messages)
from jmemory.memory.base import MemoryBase
from jmemory.memory.setup import jmemory_dir, setup_config
from jmemory.memory.storage import SQLiteManager
from jmemory.memory.utils import (
    get_fact_retrieval_messages,
    parse_messages,
    parse_vision_messages,
    remove_code_blocks,
)
from jmemory.vector_stores.qdrant import Qdrant
from jmemory.graphs.memgraph_memory import MemoryGraph
from jmemory.embeddings.huggingface import HuggingFaceEmbedding
from jmemory.llms.utils.llm_loader import LlmLoader


def capture_event(event_name: str, data: Optional[dict] = None) -> None:
    """Placeholder telemetry hook used in tests."""
    logging.debug("capture_event %s: %s", event_name, data)


def _build_filters_and_metadata(
    *,  # Enforce keyword-only arguments
    user_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    run_id: Optional[str] = None,
    actor_id: Optional[str] = None,  # For query-time filtering
    input_metadata: Optional[Dict[str, Any]] = None,
    input_filters: Optional[Dict[str, Any]] = None,
) -> tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Constructs metadata for storage and filters for querying based on session and actor identifiers.

    This helper supports multiple session identifiers (`user_id`, `agent_id`, and/or `run_id`)
    for flexible session scoping and optionally narrows queries to a specific `actor_id`. It returns two dicts:

    1. `base_metadata_template`: Used as a template for metadata when storing new memories.
       It includes all provided session identifier(s) and any `input_metadata`.
    2. `effective_query_filters`: Used for querying existing memories. It includes all
       provided session identifier(s), any `input_filters`, and a resolved actor
       identifier for targeted filtering if specified by any actor-related inputs.

    Actor filtering precedence: explicit `actor_id` arg → `filters["actor_id"]`
    This resolved actor ID is used for querying but is not added to `base_metadata_template`,
    as the actor for storage is typically derived from message content at a later stage.

    Args:
        user_id (Optional[str]): User identifier, for session scoping.
        agent_id (Optional[str]): Agent identifier, for session scoping.
        run_id (Optional[str]): Run identifier, for session scoping.
        actor_id (Optional[str]): Explicit actor identifier, used as a potential source for
            actor-specific filtering. See actor resolution precedence in the main description.
        input_metadata (Optional[Dict[str, Any]]): Base dictionary to be augmented with
            session identifiers for the storage metadata template. Defaults to an empty dict.
        input_filters (Optional[Dict[str, Any]]): Base dictionary to be augmented with
            session and actor identifiers for query filters. Defaults to an empty dict.

    Returns:
        tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing:
            - base_metadata_template (Dict[str, Any]): Metadata template for storing memories,
              scoped to the provided session(s).
            - effective_query_filters (Dict[str, Any]): Filters for querying memories,
              scoped to the provided session(s) and potentially a resolved actor.
    """

    base_metadata_template = deepcopy(input_metadata) if input_metadata else {}
    effective_query_filters = deepcopy(input_filters) if input_filters else {}

    # ---------- add all provided session ids ----------
    session_ids_provided = []

    if user_id:
        base_metadata_template["user_id"] = user_id
        effective_query_filters["user_id"] = user_id
        session_ids_provided.append("user_id")

    if agent_id:
        base_metadata_template["agent_id"] = agent_id
        effective_query_filters["agent_id"] = agent_id
        session_ids_provided.append("agent_id")

    if run_id:
        base_metadata_template["run_id"] = run_id
        effective_query_filters["run_id"] = run_id
        session_ids_provided.append("run_id")

    if not session_ids_provided:
        raise ValueError("At least one of 'user_id', 'agent_id', or 'run_id' must be provided.")

    # ---------- optional actor filter ----------
    resolved_actor_id = actor_id or effective_query_filters.get("actor_id")
    if resolved_actor_id:
        effective_query_filters["actor_id"] = resolved_actor_id

    return base_metadata_template, effective_query_filters


logger = logging.getLogger(__name__)


class Memory(MemoryBase):
    def __init__(self, config: MemoryConfig = MemoryConfig()):
        self.config = config
        self.llm = LlmLoader(self.config.llm.provider, self.config.llm.config).load()

        # Initialize vector store (Qdrant)
        self.embedder = HuggingFaceEmbedding(
            model="/models/bge-large-en-v1.5",
            model_kwargs={
                "device": "cuda:0"
            }
        )
        self.vector_store = Qdrant(
            embedding_model_dims=self.embedder.config.embedding_dims,
        )

        # Initialize graph store (Memgraph)
        self.graph_store = MemoryGraph()

    def add(self, messages: List[Dict[str, Any]], user_id: str, metadata: Optional[Dict[str, Any]] = None):
        # This is a simplified version. In a real implementation, this would be much more complex.
        # It would involve using an LLM to process the messages and update the different memory layers.
        print(f"Adding {len(messages)} messages to memory for user {user_id}")
        # For now, we'll just add the raw messages to the vector store.
        texts = [m["content"] for m in messages]
        embeddings = [self.embedder.embed(text) for text in texts]
        self.vector_store.insert(vectors=embeddings, payloads=[metadata] * len(texts), ids=[user_id] * len(texts))

    def search(self, query: str, user_id: str, limit: int = 5, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        # This is a simplified version. In a real implementation, this would be much more complex.
        # It would involve querying all six memory layers and combining the results.
        print(f"Searching memory for user {user_id} with query: {query}")
        query_embedding = self.embedder.embed(query)
        return self.vector_store.search(query=query_embedding, limit=limit, filters=filters)

    def get_all(self, user_id: str) -> List[Dict[str, Any]]:
        print(f"Getting all memories for user {user_id}")
        return self.vector_store.list(filters={"user_id": user_id})

    def update(self, memory_id: str, data: Dict[str, Any]):
        print(f"Updating memory {memory_id}")
        updated_embedding = self.embedder.embed(data)
        self.vector_store.update(vector_id=memory_id, vector=updated_embedding, payload=data)

    def delete(self, memory_id: str):
        print(f"Deleting memory {memory_id}")
        self.vector_store.delete(vector_id=memory_id)

    def delete_all(self, user_id: str):
        print(f"Deleting all memories for user {user_id}")
        # This is a simplified version. In a real implementation, this would be much more complex.
        # It would would involve deleting all memories for the user from all six memory layers.
        memories = self.get_all(user_id)
        for memory in memories:
            self.delete(memory["id"])

    def get(self, memory_id: str) -> Optional[Dict[str, Any]]:
        print(f"Getting memory {memory_id}")
        # This is a simplified version. In a real implementation, this would involve retrieving a single memory from the vector store.
        return self.vector_store.get(memory_id)

    def history(self, memory_id: str):
        raise NotImplementedError("History is not yet implemented in the new Memory Palace.")

    def reset(self):
        print("Resetting the Memory Palace.")
        self.vector_store.reset()
        self.graph_store.delete_all()
