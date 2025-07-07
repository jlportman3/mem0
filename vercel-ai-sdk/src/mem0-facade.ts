import { withoutTrailingSlash } from '@ai-sdk/provider-utils'

import { JmemoryGenericLanguageModel } from './jmemory-generic-language-model'
import { JmemoryChatModelId, JmemoryChatSettings } from './jmemory-types'
import { JmemoryProviderSettings } from './jmemory-provider'

export class Jmemory {
  readonly baseURL: string
  readonly headers?: any

  constructor(options: JmemoryProviderSettings = {
    provider: 'openai',
  }) {
    this.baseURL =
      withoutTrailingSlash(options.baseURL) ?? 'http://127.0.0.1:11434/api'

    this.headers = options.headers
  }

  private get baseConfig() {
    return {
      baseURL: this.baseURL,
      headers: this.headers,
    }
  }

  chat(modelId: JmemoryChatModelId, settings: JmemoryChatSettings = {}) {
    return new JmemoryGenericLanguageModel(modelId, settings, {
      provider: 'openai',
      modelType: 'chat',
      ...this.baseConfig,
    })
  }

  completion(modelId: JmemoryChatModelId, settings: JmemoryChatSettings = {}) {
    return new JmemoryGenericLanguageModel(modelId, settings, {
      provider: 'openai',
      modelType: 'completion',
      ...this.baseConfig,
    })
  }
}