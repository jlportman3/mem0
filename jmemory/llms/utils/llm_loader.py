from jmemory.utils.factory import LlmFactory

class LlmLoader:
    def __init__(self, provider, config):
        self.provider = provider
        self.config = config

    def load(self):
        return LlmFactory.create(self.provider, self.config)