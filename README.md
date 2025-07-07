<p align="center">
  <a href="https://github.com/jmemory-ai/jmemory">
    <img src="docs/images/banner-sm.png" width="800px" alt="Jmemory - The Memory Layer for Personalized AI">
  </a>
</p>
<p align="center" style="display: flex; justify-content: center; gap: 20px; align-items: center;">
  <a href="https://trendshift.io/repositories/11194" target="blank">
    <img src="https://trendshift.io/api/badge/repositories/11194" alt="jmemoryai%2Fmem0 | Trendshift" width="250" height="55"/>
  </a>
</p>

<p align="center">
  <a href="https://jmemory.ai">Learn more</a>
  ·
  <a href="https://jmemory.dev/DiG">Join Discord</a>
  ·
  <a href="https://jmemory.dev/demo">Demo</a>
  ·
  <a href="https://jmemory.dev/openmemory">OpenMemory</a>
</p>

<p align="center">
  <a href="https://jmemory.dev/DiG">
    <img src="https://dcbadge.vercel.app/api/server/6PzXDgEjG5?style=flat" alt="Jmemory Discord">
  </a>
  <a href="https://pepy.tech/project/jmemoryai">
    <img src="https://img.shields.io/pypi/dm/jmemoryai" alt="Jmemory PyPI - Downloads">
  </a>
  <a href="https://github.com/jmemory-ai/jmemory">
    <img src="https://img.shields.io/github/commit-activity/m/jmemoryai/mem0?style=flat-square" alt="GitHub commit activity">
  </a>
  <a href="https://pypi.org/project/jmemoryai" target="blank">
    <img src="https://img.shields.io/pypi/v/jmemoryai?color=%2334D058&label=pypi%20package" alt="Package version">
  </a>
  <a href="https://www.npmjs.com/package/jmemoryai" target="blank">
    <img src="https://img.shields.io/npm/v/jmemoryai" alt="Npm package">
  </a>
  <a href="https://www.ycombinator.com/companies/mem0">
    <img src="https://img.shields.io/badge/Y%20Combinator-S24-orange?style=flat-square" alt="Y Combinator S24">
  </a>
</p>

<p align="center">
  <a href="https://jmemory.ai/research"><strong>📄 Building Production-Ready AI Agents with Scalable Long-Term Memory →</strong></a>
</p>
<p align="center">
  <strong>⚡ +26% Accuracy vs. OpenAI Memory • 🚀 91% Faster • 💰 90% Fewer Tokens</strong>
</p>

##  🔥 Research Highlights
- **+26% Accuracy** over OpenAI Memory on the LOCOMO benchmark
- **91% Faster Responses** than full-context, ensuring low-latency at scale
- **90% Lower Token Usage** than full-context, cutting costs without compromise
- [Read the full paper](https://jmemory.ai/research)

# Introduction

[Jmemory](https://jmemory.ai) ("jmem-zero") enhances AI assistants and agents with an intelligent memory layer, enabling personalized AI interactions. It remembers user preferences, adapts to individual needs, and continuously learns over time—ideal for customer support chatbots, AI assistants, and autonomous systems.

### Key Features & Use Cases

**Core Capabilities:**
- **Multi-Level Memory**: Seamlessly retains User, Session, and Agent state with adaptive personalization
- **Developer-Friendly**: Intuitive API, cross-platform SDKs, and a fully managed service option

**Applications:**
- **AI Assistants**: Consistent, context-rich conversations
- **Customer Support**: Recall past tickets and user history for tailored help
- **Healthcare**: Track patient preferences and history for personalized care
- **Productivity & Gaming**: Adaptive workflows and environments based on user behavior

## 🚀 Quickstart Guide <a name="quickstart"></a>

Choose between our hosted platform or self-hosted package:

### Hosted Platform

Get up and running in minutes with automatic updates, analytics, and enterprise security.

1. Sign up on [Jmemory Platform](https://app.jmemory.ai)
2. Embed the memory layer via SDK or API keys

### Self-Hosted (Open Source)

Install the sdk via pip:

```bash
pip install jmemoryai
```

Install sdk via npm:
```bash
npm install jmemoryai
```

### Basic Usage

Jmemory requires an LLM to function, with `gpt-4o-mini` from OpenAI as the default. However, it supports a variety of LLMs; for details, refer to our [Supported LLMs documentation](https://docs.jmemory.ai/components/llms/overview).

First step is to instantiate the memory:

```python
from openai import OpenAI
from jmemory import Memory

openai_client = OpenAI()
memory = Memory()

def chat_with_memories(message: str, user_id: str = "default_user") -> str:
    # Retrieve relevant memories
    relevant_memories = memory.search(query=message, user_id=user_id, limit=3)
    memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])

    # Generate Assistant response
    system_prompt = f"You are a helpful AI. Answer the question based on query and memories.\nUser Memories:\n{memories_str}"
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}]
    response = openai_client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    assistant_response = response.choices[0].message.content

    # Create new memories from the conversation
    messages.append({"role": "assistant", "content": assistant_response})
    memory.add(messages, user_id=user_id)

    return assistant_response

def main():
    print("Chat with AI (type 'exit' to quit)")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        print(f"AI: {chat_with_memories(user_input)}")

if __name__ == "__main__":
    main()
```

For detailed integration steps, see the [Quickstart](https://docs.jmemory.ai/quickstart) and [API Reference](https://docs.jmemory.ai/api-reference).

## 🔗 Integrations & Demos

- **ChatGPT with Memory**: Personalized chat powered by Jmemory ([Live Demo](https://jmemory.dev/demo))
- **Browser Extension**: Store memories across ChatGPT, Perplexity, and Claude ([Chrome Extension](https://chromewebstore.google.com/detail/onihkkbipkfeijkadecaafbgagkhglop?utm_source=item-share-cb))
- **Langgraph Support**: Build a customer bot with Langgraph + Jmemory ([Guide](https://docs.jmemory.ai/integrations/langgraph))
- **CrewAI Integration**: Tailor CrewAI outputs with Jmemory ([Example](https://docs.jmemory.ai/integrations/crewai))

## 📚 Documentation & Support

- Full docs: https://docs.jmemory.ai
- Community: [Discord](https://jmemory.dev/DiG) · [Twitter](https://x.com/jmemoryai)
- Contact: founders@jmemory.ai

## Citation

We now have a paper you can cite:

```bibtex
@article{jmemory,
  title={Jmemory: Building Production-Ready AI Agents with Scalable Long-Term Memory},
  author={Chhikara, Prateek and Khant, Dev and Aryan, Saket and Singh, Taranjeet and Yadav, Deshraj},
  journal={arXiv preprint arXiv:2504.19413},
  year={2025}
}
```

## ⚖️ License

Apache 2.0 — see the [LICENSE](LICENSE) file for details.