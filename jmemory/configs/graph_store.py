from pydantic import BaseModel, Field

class GraphStoreConfig(BaseModel):
    url: str = Field("bolt://memgraph:7687", description="URL for Memgraph instance")
    username: str = Field("memgraph", description="Username for Memgraph")
    password: str = Field("memgraph", description="Password for Memgraph")
