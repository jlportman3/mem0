from pydantic import BaseModel, Field

class VectorStoreConfig(BaseModel):
    collection_name: str = Field("jmemory", description="Name of the Qdrant collection")
    path: str = Field("/qdrant/storage", description="Path to Qdrant storage")
    on_disk: bool = Field(True, description="Whether to store Qdrant data on disk")
