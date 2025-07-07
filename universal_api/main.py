

import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
import litellm
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from jmemory.memory.main import Memory
from jmemory.configs.base import MemoryConfig

# Initialize FastAPI app
app = FastAPI(
    title="Universal LLM API",
    description="An OpenAI-compatible API that routes requests to any major LLM provider.",
)

# Initialize jmemory
jmemory = Memory(MemoryConfig())

# --- Pydantic Models for API ---

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    stream: Optional[bool] = False
    # Add other OpenAI-compatible parameters as needed
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None

# --- jmemory Pre/Post-processing Stubs ---

async def jmemory_preprocess(request_data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """
    Jmemory pre-processing.
    Enriches `messages` with memory.
    """
    print("--- Jmemory Pre-processing ---")
    # For now, we'll just add a simple memory retrieval.
    # In a real implementation, this would involve more sophisticated memory retrieval and injection.
    retrieved_memories = jmemory.search(query=request_data["messages"][-1]["content"], user_id=user_id)
    if retrieved_memories:
        memory_context = "\nRelevant memories:\n" + "\n".join([m["memory"] for m in retrieved_memories])
        request_data["messages"].insert(0, {"role": "system", "content": memory_context})
    return request_data

async def jmemory_postprocess(response: Any, user_id: str):
    """
    Jmemory post-processing.
    Updates memory based on the conversation.
    """
    print("--- Jmemory Post-processing ---")
    # For now, we'll just add the last user message and the AI's response to memory.
    # In a real implementation, this would involve more sophisticated fact extraction and memory updates.
    last_user_message = response.request.messages[-1]["content"]
    ai_response = response.choices[0].message.content
    jmemory.add(messages=[{"role": "user", "content": last_user_message}, {"role": "assistant", "content": ai_response}], user_id=user_id)
    return response

# --- API Endpoint ---

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """
    OpenAI-compatible chat completions endpoint.
    """
    try:
        request_data = request.model_dump()

        # For demonstration, using a static user_id. In a real app, this would come from auth.
        user_id = "test_user"

        # 1. Jmemory Pre-processing
        enriched_data = await jmemory_preprocess(request_data, user_id)

        # 2. Route to LLM provider via LiteLLM
        if enriched_data.get("stream"):
            # Handle streaming responses
            async def stream_generator():
                streaming_response = await litellm.acompletion(**enriched_data, stream=True)
                async for chunk in streaming_response:
            # 6. Jmemory Post-processing (can be done chunk-by-chunk or after completion)
            # Note: Post-processing for streaming is more complex and might require accumulating chunks.
            # For simplicity, this example processes each chunk, but a full implementation
            # would likely process the complete streamed response.
                    processed_chunk = await jmemory_postprocess(chunk, user_id)
                    yield f"data: {processed_chunk.model_dump_json()}\n\n"
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(stream_generator(), media_type="text/event-stream")
        else:
            # Handle non-streaming responses
            response = await litellm.acompletion(**enriched_data)
            
            # 6. Jmemory Post-processing
            final_response = await jmemory_postprocess(response, user_id)
            
            return JSONResponse(content=final_response.model_dump())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Universal LLM API is running."}
