import { MemoryClient } from "./jmemory";
import type * as JmemoryTypes from "./jmemory.types";

// Re-export all types from mem0.types
export type {
  JmemoryOptions,
  ProjectOptions,
  Jmemory,
  JmemoryHistory,
  JmemoryUpdateBody,
  ProjectResponse,
  PromptUpdatePayload,
  JmemorySearchOptions,
  Webhook,
  WebhookPayload,
  Messages,
  Message,
  AllUsers,
  User,
  FeedbackPayload,
  Feedback,
} from "./jmemory.types";

// Export the main client
export { MemoryClient };
export default MemoryClient;
