from typing import Optional

from pydantic import BaseModel, Field, field_validator


class EmbedderConfig(BaseModel):
    provider: str = Field(
        description="Provider of the embedding model (must be 'huggingface')",
        default="huggingface",
    )
    config: dict = Field(
        description="Configuration for the Hugging Face embedding model",
        default_factory=lambda: {
            "model": "/models/bge-large-en-v1.5",
            "model_kwargs": {"device": "cuda:0"},
        },
    )

    @field_validator("provider")
    def validate_provider(cls, v):
        if v != "huggingface":
            raise ValueError("Embedding provider is fixed to 'huggingface'")
        return v

    @field_validator("config")
    def validate_config(cls, v, values):
        return v
