import logging
import threading
from typing import List, Optional, Union

import httpx

import jmemory

from jmemory import Memory
from jmemory.configs.enums import MemoryType
from jmemory.configs.prompts import MEMORY_ANSWER_PROMPT

logger = logging.getLogger(__name__)


class Jmemory:
    def __init__(
        self,
        config: Optional[dict] = None,
    ):
        self.jmemory_client = Memory.from_config(config) if config else Memory()

        self.chat = Chat(self.jmemory_client)


class Chat:
    def __init__(self, jmemory_client):
        self.completions = Completions(jmemory_client)


class Completions:
    def __init__(self, jmemory_client):
        self.jmemory_client = jmemory_client

    def create(
        self,
        model: str,
        messages: List = [],
        # Mem0 arguments
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        run_id: Optional[str] = None,
        metadata: Optional[dict] = None,
        filters: Optional[dict] = None,
        limit: Optional[int] = 10,
        # LLM arguments
        timeout: Optional[Union[float, str, httpx.Timeout]] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        n: Optional[int] = None,
        stream: Optional[bool] = None,
        stream_options: Optional[dict] = None,
        stop=None,
        max_tokens: Optional[int] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        logit_bias: Optional[dict] = None,
        user: Optional[str] = None,
        # openai v1.0+ new params
        response_format: Optional[dict] = None,
        seed: Optional[int] = None,
        tools: Optional[List] = None,
        tool_choice: Optional[Union[str, dict]] = None,
        logprobs: Optional[bool] = None,
        top_logprobs: Optional[int] = None,
        parallel_tool_calls: Optional[bool] = None,
        deployment_id=None,
        extra_headers: Optional[dict] = None,
        # soon to be deprecated params by OpenAI
        functions: Optional[List] = None,
        function_call: Optional[str] = None,
        # set api_base, api_version, api_key
        base_url: Optional[str] = None,
        api_version: Optional[str] = None,
        api_key: Optional[str] = None,
        model_list: Optional[list] = None,  # pass in a list of api_base,keys, etc.
    ):
        if not any([user_id, agent_id, run_id]):
            raise ValueError("One of user_id, agent_id, run_id must be provided")

        prepared_messages = self._prepare_messages(messages)
        if prepared_messages[-1]["role"] == "user":
            self._async_add_to_memory(messages, user_id, agent_id, run_id, metadata, filters)
            relevant_memories = self._fetch_relevant_memories(messages, user_id, agent_id, run_id, filters, limit)
            logger.debug(f"Retrieved {len(relevant_memories)} relevant memories")
            prepared_messages[-1]["content"] = self._format_query_with_memories(messages, relevant_memories)

        response = litellm.completion(
            model=model,
            messages=prepared_messages,
            temperature=temperature,
            top_p=top_p,
            n=n,
            timeout=timeout,
            stream=stream,
            stream_options=stream_options,
            stop=stop,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            logit_bias=logit_bias,
            user=user,
            response_format=response_format,
            seed=seed,
            tools=tools,
            tool_choice=tool_choice,
            logprobs=logprobs,
            top_logprobs=top_logprobs,
            parallel_tool_calls=parallel_tool_calls,
            deployment_id=deployment_id,
            extra_headers=extra_headers,
            functions=functions,
            function_call=function_call,
            base_url=base_url,
            api_version=api_version,
            api_key=api_key,
            model_list=model_list,
        )

        if not stream:
            try:
                assistant_msg = response.choices[0].message
            except AttributeError:
                assistant_msg = response["choices"][0]["message"]
            self._async_add_to_memory(
                [assistant_msg],
                user_id=user_id,
                agent_id=agent_id,
                run_id=run_id,
                metadata=metadata,
                filters=filters,
            )

        return response

    def _prepare_messages(self, messages: List[dict]) -> List[dict]:
        if not messages or messages[0]["role"] != "system":
            return [{"role": "system", "content": MEMORY_ANSWER_PROMPT}] + messages
        return messages

    def _async_add_to_memory(self, messages, user_id, agent_id, run_id, metadata, filters):
        def add_task():
            logger.debug("Adding to memory asynchronously")
            self.jmemory_client.add(
                messages=messages,
                user_id=user_id,
                agent_id=agent_id,
                run_id=run_id,
                metadata=metadata,
                filters=filters,
                memory_type=MemoryType.SHORT_TERM.value,
            )

        threading.Thread(target=add_task, daemon=True).start()

    def _fetch_relevant_memories(self, messages, user_id, agent_id, run_id, filters, limit):
        # Currently, only pass the last 6 messages to the search API to prevent long query
        message_input = [f"{message['role']}: {message['content']}" for message in messages][-6:]
        # TODO: Make it better by summarizing the past conversation
        return self.jmemory_client.search(
            query="\n".join(message_input),
            user_id=user_id,
            agent_id=agent_id,
            run_id=run_id,
            filters=filters,
            limit=limit,
        )

    def _format_query_with_memories(self, messages, relevant_memories):
        # Check if self.jmemory_client is an instance of Memory or MemoryClient

        entities = []
        memories_text = "\n".join(memory["memory"] for memory in relevant_memories["results"])
        if relevant_memories.get("relations"):
            entities = [entity for entity in relevant_memories["relations"]]
        return f"- Relevant Memories/Facts: {memories_text}\n\n- Entities: {entities}\n\n- User Question: {messages[-1]['content']}"
