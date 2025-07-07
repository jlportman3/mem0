import importlib
from typing import Optional

from jmemory.configs.embeddings.base import BaseEmbedderConfig
from jmemory.configs.llms.base import BaseLlmConfig
from jmemory.embeddings.mock import MockEmbeddings


def load_class(class_type):
    module_path, class_name = class_type.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


class LlmFactory:
    provider_to_class = {
        "ollama": "jmemory.llms.ollama.OllamaLLM",
        "openai": "jmemory.llms.openai.OpenAILLM",
        "groq": "jmemory.llms.groq.GroqLLM",
        "together": "jmemory.llms.together.TogetherLLM",
        "aws_bedrock": "jmemory.llms.aws_bedrock.AWSBedrockLLM",
        "litellm": "jmemory.llms.litellm.LiteLLM",
        "azure_openai": "jmemory.llms.azure_openai.AzureOpenAILLM",
        "openai_structured": "jmemory.llms.openai_structured.OpenAIStructuredLLM",
        "anthropic": "jmemory.llms.anthropic.AnthropicLLM",
        "azure_openai_structured": "jmemory.llms.azure_openai_structured.AzureOpenAIStructuredLLM",
        "gemini": "jmemory.llms.gemini.GeminiLLM",
        "deepseek": "jmemory.llms.deepseek.DeepSeekLLM",
        "xai": "jmemory.llms.xai.XAILLM",
        "sarvam": "jmemory.llms.sarvam.SarvamLLM",
        "lmstudio": "jmemory.llms.lmstudio.LMStudioLLM",
        "langchain": "jmemory.llms.langchain.LangchainLLM",
    }

    @classmethod
    def create(cls, provider_name, config):
        class_type = cls.provider_to_class.get(provider_name)
        if class_type:
            llm_instance = load_class(class_type)
            base_config = BaseLlmConfig(**config)
            return llm_instance(base_config)
        else:
            raise ValueError(f"Unsupported Llm provider: {provider_name}")


class EmbedderFactory:
    provider_to_class = {
        "openai": "jmemory.embeddings.openai.OpenAIEmbedding",
        "ollama": "jmemory.embeddings.ollama.OllamaEmbedding",
        "huggingface": "jmemory.embeddings.huggingface.HuggingFaceEmbedding",
        "azure_openai": "jmemory.embeddings.azure_openai.AzureOpenAIEmbedding",
        "gemini": "jmemory.embeddings.gemini.GoogleGenAIEmbedding",
        "vertexai": "jmemory.embeddings.vertexai.VertexAIEmbedding",
        "together": "jmemory.embeddings.together.TogetherEmbedding",
        "lmstudio": "jmemory.embeddings.lmstudio.LMStudioEmbedding",
        "langchain": "jmemory.embeddings.langchain.LangchainEmbedding",
        "aws_bedrock": "jmemory.embeddings.aws_bedrock.AWSBedrockEmbedding",
    }

    @classmethod
    def create(cls, provider_name, config, vector_config: Optional[dict]):
        if provider_name == "upstash_vector" and vector_config and vector_config.enable_embeddings:
            return MockEmbeddings()
        class_type = cls.provider_to_class.get(provider_name)
        if class_type:
            embedder_instance = load_class(class_type)
            base_config = BaseEmbedderConfig(**config)
            return embedder_instance(base_config)
        else:
            raise ValueError(f"Unsupported Embedder provider: {provider_name}")
