import { JmemoryProviderSettings } from "./jmemory-provider";
import { OpenAIChatSettings } from "@ai-sdk/openai/internal";
import { AnthropicMessagesSettings } from "@ai-sdk/anthropic/internal";
import {
  LanguageModelV1
} from "@ai-sdk/provider";

export type JmemoryChatModelId =
  | (string & NonNullable<unknown>);

export interface JmemoryConfigSettings {
  user_id?: string;
  app_id?: string;
  agent_id?: string;
  run_id?: string;
  org_name?: string;
  project_name?: string;
  org_id?: string;
  project_id?: string;
  metadata?: Record<string, any>;
  filters?: Record<string, any>;
  infer?: boolean;
  page?: number;
  page_size?: number;
  jmemoryApiKey?: string;
  top_k?: number;
  threshold?: number;
  rerank?: boolean;
  enable_graph?: boolean;
  output_format?: string;
  filter_memories?: boolean;
}

export interface JmemoryChatConfig extends JmemoryConfigSettings, JmemoryProviderSettings {}

export interface JmemoryConfig extends JmemoryConfigSettings {}
export interface JmemoryChatSettings extends OpenAIChatSettings, AnthropicMessagesSettings, JmemoryConfigSettings {}

export interface JmemoryStreamResponse extends Awaited<ReturnType<LanguageModelV1['doStream']>> {
  memories: any;
}
