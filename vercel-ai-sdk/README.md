# Jmemory AI SDK Provider

The **Jmemory AI SDK Provider** is a community-maintained library developed by [Jmemory](https://jmemory.ai/) to integrate with the Vercel AI SDK. This library brings enhanced AI interaction capabilities to your applications by introducing persistent memory functionality. With Jmemory, language model conversations gain memory, enabling more contextualized and personalized responses based on past interactions.

Discover more of **Jmemory** on [GitHub](https://github.com/jmemoryai).
Explore the [Jmemory Documentation](https://docs.jmemory.ai/overview) to gain deeper control and flexibility in managing your memories.

For detailed information on using the Vercel AI SDK, refer to Vercel’s [API Reference](https://sdk.vercel.ai/docs/reference) and [Documentation](https://sdk.vercel.ai/docs).

## Features

- 🧠 Persistent memory storage for AI conversations
- 🔄 Seamless integration with Vercel AI SDK
- 🚀 Support for multiple LLM providers
- 📝 Rich message format support
- ⚡ Streaming capabilities
- 🔍 Context-aware responses

## Installation

```bash
npm install @jmemory/vercel-ai-provider
```

## Before We Begin

### Setting Up Jmemory

1. Obtain your [Jmemory API Key](https://app.jmemory.ai/dashboard/api-keys) from the Jmemory dashboard.

2. Initialize the Mem0 Client:

```typescript
import { createJmemory } from "@jmemory/vercel-ai-provider";

const jmemory = createJmemory({
  provider: "openai",
  jmemoryApiKey: "m0-xxx",
  apiKey: "openai-api-key",
  config: {
    compatibility: "strict",
    // Additional model-specific configuration options can be added here.
  },
});
```

### Note
By default, the `openai` provider is used, so specifying it is optional:
```typescript
const jmemory = createJmemory();
```
For better security, consider setting `JMEMORY_API_KEY` and `OPENAI_API_KEY` as environment variables.

3. Add Memories to Enhance Context:

```typescript
import { LanguageModelV1Prompt } from "ai";
import { addMemories } from "@mem0/vercel-ai-provider";

const messages: LanguageModelV1Prompt = [
  {
    role: "user",
    content: [
      { type: "text", text: "I love red cars." },
      { type: "text", text: "I like Toyota Cars." },
      { type: "text", text: "I prefer SUVs." },
    ],
  },
];

await addMemories(messages, { user_id: "borat" });
```

These memories are now stored in your profile. You can view and manage them on the [Jmemory Dashboard](https://app.jmemory.ai/dashboard/users).

### Note:

For standalone features, such as `addMemories` and `retrieveMemories`,
you must either set `JMEMORY_API_KEY` as an environment variable or pass it directly in the function call.

Example:

```typescript
await addMemories(messages, { user_id: "borat", jmemoryApiKey: "m0-xxx", org_id: "org_xx", project_id: "proj_xx" });
await retrieveMemories(prompt, { user_id: "borat", jmemoryApiKey: "m0-xxx", org_id: "org_xx", project_id: "proj_xx" });
await getMemories(prompt, { user_id: "borat", jmemoryApiKey: "m0-xxx", org_id: "org_xx", project_id: "proj_xx" });
```

### Note:

`retrieveMemories` enriches the prompt with relevant memories from your profile, while `getMemories` returns the memories in array format which can be used for further processing.

## Usage Examples

### 1. Basic Text Generation with Memory Context

```typescript
import { generateText } from "ai";
import { createJmemory } from "@mem0/vercel-ai-provider";

const jmemory = createJmemory();

const { text } = await generateText({
  model: jmemory("gpt-4-turbo", {
    user_id: "borat",
  }),
  prompt: "Suggest me a good car to buy!",
});
```

### 2. Combining OpenAI Provider with Memory Utils

```typescript
import { generateText } from "ai";
import { openai } from "@ai-sdk/openai";
import { retrieveMemories } from "@mem0/vercel-ai-provider";

const prompt = "Suggest me a good car to buy.";
const memories = await retrieveMemories(prompt, { user_id: "borat" });

const { text } = await generateText({
  model: openai("gpt-4-turbo"),
  prompt: prompt,
  system: memories,
});
```

### 3. Structured Message Format with Memory

```typescript
import { generateText } from "ai";
import { createJmemory } from "@mem0/vercel-ai-provider";

const jmemory = createJmemory();

const { text } = await generateText({
  model: jmemory("gpt-4-turbo", {
    user_id: "borat",
  }),
  messages: [
    {
      role: "user",
      content: [
        { type: "text", text: "Suggest me a good car to buy." },
        { type: "text", text: "Why is it better than the other cars for me?" },
        { type: "text", text: "Give options for every price range." },
      ],
    },
  ],
});
```

### 4. Advanced Memory Integration with OpenAI

```typescript
import { generateText, LanguageModelV1Prompt } from "ai";
import { openai } from "@ai-sdk/openai";
import { retrieveMemories } from "@mem0/vercel-ai-provider";

// New format using system parameter for memory context
const messages: LanguageModelV1Prompt = [
  {
    role: "user",
    content: [
      { type: "text", text: "Suggest me a good car to buy." },
      { type: "text", text: "Why is it better than the other cars for me?" },
      { type: "text", text: "Give options for every price range." },
    ],
  },
];

const memories = await retrieveMemories(messages, { user_id: "borat" });

const { text } = await generateText({
  model: openai("gpt-4-turbo"),
  messages: messages,
  system: memories,
});
```

### 5. Streaming Responses with Memory Context

```typescript
import { streamText } from "ai";
import { createJmemory } from "@mem0/vercel-ai-provider";

const jmemory = createJmemory();

const { textStream } = await streamText({
  model: jmemory("gpt-4-turbo", {
    user_id: "borat",
  }),
  prompt:
    "Suggest me a good car to buy! Why is it better than the other cars for me? Give options for every price range.",
});

for await (const textPart of textStream) {
  process.stdout.write(textPart);
}
```

## Core Functions

- `createJmemory()`: Initializes a new jmemory provider instance with optional configuration
- `retrieveMemories()`: Enriches prompts with relevant memories
- `addMemories()`: Add memories to your profile
- `getMemories()`: Get memories from your profile in array format

## Configuration Options

```typescript
const jmemory = createJmemory({
  config: {
    ...
    // Additional model-specific configuration options can be added here.
  },
});
```

## Best Practices

1. **User Identification**: Always provide a unique `user_id` identifier for consistent memory retrieval
2. **Context Management**: Use appropriate context window sizes to balance performance and memory
3. **Error Handling**: Implement proper error handling for memory operations
4. **Memory Cleanup**: Regularly clean up unused memory contexts to optimize performance

We also have support for `agent_id`, `app_id`, and `run_id`. Refer [Docs](https://docs.jmemory.ai/api-reference/memory/add-memories).

## Notes

- Requires proper API key configuration for underlying providers (e.g., OpenAI)
- Memory features depend on proper user identification via `user_id`
- Supports both streaming and non-streaming responses
- Compatible with all Vercel AI SDK features and patterns
