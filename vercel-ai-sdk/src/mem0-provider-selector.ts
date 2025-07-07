import { JmemoryProviderSettings } from "./jmemory-provider";
import JmemoryAITextGenerator, { ProviderSettings } from "./provider-response-provider";
import { LanguageModelV1 } from "ai";

class JmemoryClassSelector {
    modelId: string;
    provider_wrapper: string;
    config: JmemoryProviderSettings;
    provider_config?: ProviderSettings;
    static supportedProviders = ["openai", "anthropic", "cohere", "groq", "google"];

    constructor(modelId: string, config: JmemoryProviderSettings, provider_config?: ProviderSettings) {
        this.modelId = modelId;
        this.provider_wrapper = config.provider || "openai";
        this.provider_config = provider_config;
        if(config) this.config = config;
        else this.config = {
            provider: this.provider_wrapper,
        };

        // Check if provider_wrapper is supported
        if (!JmemoryClassSelector.supportedProviders.includes(this.provider_wrapper)) {
            throw new Error(`Model not supported: ${this.provider_wrapper}`);
        }
    }

    createProvider(): LanguageModelV1 {
        return new JmemoryAITextGenerator(this.modelId, this.config , this.provider_config || {});
    }
}

export { JmemoryClassSelector };
