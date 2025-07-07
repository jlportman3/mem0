import logging
import os
from typing import Literal, Optional

from sentence_transformers import SentenceTransformer

from jmemory.configs.embeddings.base import BaseEmbedderConfig
from jmemory.embeddings.base import EmbeddingBase

logging.getLogger("transformers").setLevel(logging.WARNING)
logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
logging.getLogger("huggingface_hub").setLevel(logging.WARNING)


class HuggingFaceEmbedding(EmbeddingBase):
    def __init__(self, config: Optional[BaseEmbedderConfig] = None, model: str = "/models/bge-large-en-v1.5", model_kwargs: Optional[dict] = None):
        super().__init__(config)

        self.config.model = model
        self.config.model_kwargs = model_kwargs or {}

        # Try to load from cache first, then download if needed
        model_path = self._get_or_download_model(self.config.model)
        self.model = SentenceTransformer(model_path, **self.config.model_kwargs)

        self.config.embedding_dims = self.config.embedding_dims or self.model.get_sentence_embedding_dimension()

    def _get_or_download_model(self, model_path: str) -> str:
        """
        Get model from cache or download from HuggingFace.
        
        Args:
            model_path: Local path or HuggingFace model name
            
        Returns:
            str: Path to use for loading the model
        """
        # If it's a local path and exists, use it
        if os.path.exists(model_path):
            return model_path
            
        # If it's a local path but doesn't exist, try to map to HuggingFace name
        if model_path.startswith("/models/"):
            hf_model_name = self._local_to_hf_name(model_path)
            if hf_model_name:
                print(f"Local model path {model_path} not found, downloading {hf_model_name} from HuggingFace...")
                # Download and cache
                temp_model = SentenceTransformer(hf_model_name)
                # Create cache directory if it doesn't exist
                os.makedirs(os.path.dirname(model_path), exist_ok=True)
                # Save to cache location
                temp_model.save(model_path)
                print(f"Model cached to {model_path}")
                return model_path
        
        # Otherwise assume it's a HuggingFace model name
        return model_path
    
    def _local_to_hf_name(self, local_path: str) -> Optional[str]:
        """Map local model paths to HuggingFace model names."""
        mapping = {
            "/models/bge-large-en-v1.5": "BAAI/bge-large-en-v1.5",
            "/models/bge-base-en-v1.5": "BAAI/bge-base-en-v1.5",
            "/models/bge-small-en-v1.5": "BAAI/bge-small-en-v1.5",
        }
        return mapping.get(local_path)

    def embed(self, text, memory_action: Optional[Literal["add", "search", "update"]] = None):
        """
        Get the embedding for the given text using Hugging Face.

        Args:
            text (str): The text to embed.
            memory_action (optional): The type of embedding to use. Must be one of "add", "search", or "update". Defaults to None.
        Returns:
            list: The embedding vector.
        """
        return self.model.encode(text, convert_to_numpy=True).tolist()
