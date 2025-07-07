import { LanguageModelV1, ProviderV1 } from "@ai-sdk/provider";
import { loadApiKey, withoutTrailingSlash } from "@ai-sdk/provider-utils";
import { JmemoryChatModelId, JmemoryChatSettings, JmemoryConfig } from "./jmemory-types";
import { OpenAIProviderSettings } from "@ai-sdk/openai";
import { JmemoryGenericLanguageModel } from "./jmemory-generic-language-model";
import { OpenAIChatSettings } from "@ai-sdk/openai/internal";
import { AnthropicMessagesSettings } from "@ai-sdk/anthropic/internal";
import { AnthropicProviderSettings } from "@ai-sdk/anthropic";

export interface JmemoryProvider extends ProviderV1 {
  (modelId: JmemoryChatModelId, settings?: JmemoryChatSettings): LanguageModelV1;

  chat(modelId: JmemoryChatModelId, settings?: JmemoryChatSettings): LanguageModelV1;
  completion(modelId: JmemoryChatModelId, settings?: JmemoryChatSettings): LanguageModelV1;

  languageModel(
    modelId: JmemoryChatModelId,
    settings?: JmemoryChatSettings
  ): LanguageModelV1;
}

export interface JmemoryProviderSettings
  extends OpenAIChatSettings,
    AnthropicMessagesSettings {
  baseURL?: string;
  /**
   * Custom fetch implementation. You can use it as a middleware to intercept
   * requests or to provide a custom fetch implementation for e.g. testing
   */
  fetch?: typeof fetch;
  /**
   * @internal
   */
  generateId?: () => string;
  /**
   * Custom headers to include in the requests.
   */
  headers?: Record<string, string>;
  name?: string;
  jmemoryApiKey?: string;
  apiKey?: string;
  provider?: string;
  modelType?: "completion" | "chat";
  jmemoryConfig?: JmemoryConfig;

  /**
   * The configuration for the provider.
   */
  config?: OpenAIProviderSettings | AnthropicProviderSettings;
}

export function createJmemory(
  options: Mem0ProviderSettings = {
    provider: "openai",
  }
): JmemoryProvider {
  const baseURL =
    withoutTrailingSlash(options.baseURL) ?? "http://api.openai.com";
  const getHeaders = () => ({
    ...options.headers,
  });

  const createGenericModel = (
    modelId: JmemoryChatModelId,
    settings: JmemoryChatSettings = {}
  ) =>
    new JmemoryGenericLanguageModel(
      modelId,
      settings,
      {
        baseURL,
        fetch: options.fetch,
        headers: getHeaders(),
        provider: options.provider || "openai",
        name: options.name,
        jmemoryApiKey: options.jmemoryApiKey,
        apiKey: options.apiKey,
        jmemoryConfig: options.jmemoryConfig,
      },
      options.config
    );

  const createCompletionModel = (
    modelId: JmemoryChatModelId,
    settings: JmemoryChatSettings = {}
  ) =>
    new JmemoryGenericLanguageModel(
      modelId,
      settings,
      {
        baseURL,
        fetch: options.fetch,
        headers: getHeaders(),
        provider: options.provider || "openai",
        name: options.name,
        jmemoryApiKey: options.jmemoryApiKey,
        apiKey: options.apiKey,
        jmemoryConfig: options.jmemoryConfig,
        modelType: "completion",
      },
      options.config
    );

  const createChatModel = (
    modelId: JmemoryChatModelId,
    settings: JmemoryChatSettings = {}
  ) =>
    new JmemoryGenericLanguageModel(
      modelId,
      settings,
      {
        baseURL,
        fetch: options.fetch,
        headers: getHeaders(),
        provider: options.provider || "openai",
        name: options.name,
        jmemoryApiKey: options.jmemoryApiKey,
        apiKey: options.apiKey,
        jmemoryConfig: options.jmemoryConfig,
        modelType: "completion",
      },
      options.config
    );

  const provider = function (
    modelId: JmemoryChatModelId,
    settings: JmemoryChatSettings = {}
  ) {
    if (new.target) {
      throw new Error(
        "The Jmemory model function cannot be called with the new keyword."
      );
    }

    return createGenericModel(modelId, settings);
  };

  provider.languageModel = createGenericModel;
  provider.completion = createCompletionModel;
  provider.chat = createChatModel;

  return provider as unknown as JmemoryProvider;
}

export const jmemory = createJmemory();
