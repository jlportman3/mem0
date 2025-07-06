from enum import Enum


class MemoryType(Enum):
    SHORT_TERM = "short_term_memory"
    MEDIUM_TERM = "medium_term_memory"
    LONG_TERM = "long_term_memory"
    SEMANTIC = "semantic_memory"
    EPISODIC = "episodic_memory"
    PROCEDURAL = "procedural_memory"
