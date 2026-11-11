# Cost Optimization

## 1. Select the proper model
    - cheaper model, with less reasoning may produce less quality outputs
    - there is LLM routers that evaluate on-the-flight

### Models Prices
<!-- MODEL_PRICES_START -->
> [!NOTE]
> **Prices updated:** 2026-11-10 23:00 UTC | **Unit:** USD per 1 Million tokens ($/1M tokens).
> Source: Real-time provider pricing aggregated via OpenRouter API.

| Provider | Model | Input ($/1M) | Output ($/1M) | Context | Tier / Key Capabilities |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Anthropic** | Claude Haiku 5.5 | $0.10 | $0.50 | 1M | Ultra-fast & economical |
| **Anthropic** | Claude Sonnet 5 | $2.00 | $10.00 | 1M | Balanced intelligence & coding |
| **Anthropic** | Claude Opus 5 | $5.00 | $25.00 | 1M | Top-tier deep reasoning |
| **Cohere** | Command R (08-2024) | $0.15 | $0.60 | 128k | Cost-effective enterprise RAG |
| **Cohere** | Command A+ | $0.30 | $1.50 | 192k | Multimodal enterprise tier |
| **Cohere** | Command R+ (08-2024) | $2.50 | $10.00 | 128k | Enterprise RAG flagship |
| **DeepSeek** | DeepSeek V4.1 Flash | $0.30 | $1.20 | 1M | High-speed budget tier |
| **DeepSeek** | DeepSeek V3 | $0.32 | $0.89 | 163k | High-performance general open weights |
| **DeepSeek** | R1 0528 | $0.50 | $2.15 | 163k | Advanced reasoning & math/code |
| **Google** | Gemini 2.5 Flash Lite | $0.10 | $0.40 | 1M | Ultra low-cost & high throughput |
| **Google** | Gemini 2.5 Flash | $0.30 | $2.50 | 1M | High-speed multimodal workhorse |
| **Google** | Gemini 2.5 Pro | $1.25 | $10.00 | 1M | Flagship reasoning & 1M context |
| **Meta** | Llama 3.1 8B Instruct | $0.02 | $0.04 | 131k | Lightweight low-latency open weights (8B) |
| **Meta** | Llama 3.3 70B Instruct | $0.71 | $0.71 | 131k | Flagship open weights (70B) |
| **Meta** | Llama 3.1 70B Instruct | $0.72 | $0.72 | 131k | High-capability open weights (70B) |
| **Mistral AI** | Mistral Small 3.2 24B | $0.10 | $0.30 | 256k | Efficient enterprise tier |
| **Mistral AI** | Codestral 2508 | $0.30 | $0.90 | 256k | Code generation specialist |
| **Mistral AI** | Mistral Large | $2.00 | $6.00 | 128k | Flagship multilingual reasoning |
| **OpenAI** | GPT-4o-mini | $0.15 | $0.60 | 128k | High-efficiency fast tier |
| **OpenAI** | GPT-4.1 Mini | $0.40 | $1.60 | 1M | Affordable general purpose |
| **OpenAI** | o3 | $2.00 | $8.00 | 200k | Advanced reasoning & complex tasks |
| **OpenAI** | GPT-4.1 | $2.00 | $8.00 | 1M | High-capability general purpose |
| **OpenAI** | GPT-4o | $2.50 | $10.00 | 128k | Flagship multimodal & vision |
| **Qwen** | Qwen2.5 7B Instruct | $0.10 | $0.20 | 32k | Fast & lightweight open weights (7B) |
| **Qwen** | Qwen2.5 72B Instruct | $0.36 | $0.40 | 32k | Flagship open-weight general (72B) |
| **Qwen** | Qwen2.5 Coder 32B Instruct | $0.66 | $1.00 | 32k | Open-weight code specialist (32B) |
| **xAI** | Grok 4.7 | $2.00 | $6.00 | 500k | Flagship reasoning & 500k context |
| **xAI** | Grok 4.5 | $2.00 | $6.00 | 500k | High-performance reasoning |

**Quick Cost Insights:**
- **Lowest input cost:** `Llama 3.1 8B Instruct` (Meta) at $0.02 / 1M tokens.
- **Most affordable reasoning:** `R1 0528` (DeepSeek) at $0.50 / 1M tokens.
- **Largest context window:** `DeepSeek V4.1 Flash` (DeepSeek) with 1M tokens.
<!-- MODEL_PRICES_END -->

### References 

- https://dev.to/bd_perez/10-ways-to-reduce-your-llm-api-costs-2l33