from datetime import datetime

MEMORY_ANSWER_PROMPT = """You are a helpful AI assistant.
You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of the tools [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

"""

PROCEDURAL_MEMORY_SYSTEM_PROMPT = """You are an AI assistant that helps users remember and organize information.
You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of the tools [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

"""

def get_update_memory_messages(memory_type: str, current_date: datetime):
    return [
        {"role": "system", "content": f"You are an AI assistant that helps users remember and organize information. Current date: {current_date}"},
        {"role": "user", "content": f"Update the {memory_type} memory."}
    ]