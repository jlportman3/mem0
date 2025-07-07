You are tasked with building a universal LLM wrapper that exposes an OpenAI-compatible API. The system must support routing to any major LLM provider and fully decouple memory handling (via Mem0) from inference. Mem0 will handle all memory pre- and post-processing using its own internal LLMs. The wrapped chat model is separate and can be chosen dynamically.

Supported providers include (but are not limited to): OpenAI, OpenRouter, Groq, Google Gemini, Anthropic, and Mistral. The system must allow selecting any model per request (e.g., `gpt-4o`, `claude-3-sonnet`, `mixtral-8x7b`, etc).

Flow:

1. User sends a standard OpenAI-compatible request (e.g., `/v1/chat/completions`) with prompt and parameters.
2. API authenticates the user and forwards the request to Mem0 for pre-processing.
3. Mem0 enriches the prompt by retrieving and injecting relevant short-term, mid-term, long-term, episodic, semantic, and procedural memory.
4. The enriched prompt is routed to the selected external chat model via a provider-specific adapter.
5. The model generates a response. No memory logic is involved here.
6. The raw response is passed back through Mem0 for post-processing:

   * Logs the conversation
   * Extracts structured information (facts, decisions, entities, timelines, behaviors)
   * Updates memory layers accordingly
7. Final response is returned to the user in OpenAI-compatible format, with optional support for streaming.

Memory System Design:

* Short-Term Memory: volatile, recent tokens from the current and immediately previous sessions (up to 24 hours); serves for conversational continuity and local state.
* Mid-Term Memory: persistent session summaries and extracted facts with time decay; used to reinforce relevant info after a few exposures.
* Long-Term Memory: stable, high-value information with repetition-based promotion; immutable unless edited or deleted by the user.
* Episodic Memory: timeline of user interactions, commands, and results with full context and timestamps; supports "what happened when" queries.
* Semantic Memory: abstracted knowledge learned from the user (e.g., definitions, relationships, taxonomies); used for reasoning and inference.
* Procedural Memory: observed or instructed sequences of tasks, commands, habits, workflows; supports "how-to" execution, automation, and pattern recall.

The entire memory system is modeled as a **Memory Palace**—a dynamic, navigable graph where concepts, facts, episodes, and procedures are represented as interconnected nodes. Users can start from a single memory, idea, or concept and walk forward or backward through their personal graph of knowledge and experiences. This enables retrieval not only by keyword or timestamp, but by **associative linkage**, **contextual relevance**, and **structural proximity**.

Multimodal Capability:

This system is being built with future ingestion of **multimodal data** in mind. Images, video, audio, documents, and structured files will all be processed, embedded, and linked to the memory graph—retaining modality, timestamp, source, and relevance. Relationships between modalities (e.g., "this image was shown during that conversation") will be treated as first-class memory connections.

Nothing is to be discarded arbitrarily. All memory persists unless explicitly deleted by user instruction. The system is designed to mimic a human being with eidetic recall and an ever-expanding, richly connected mental landscape.
