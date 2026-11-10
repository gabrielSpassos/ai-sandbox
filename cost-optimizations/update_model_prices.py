#!/usr/bin/env python3
"""
update_model_prices.py

Fetches the latest LLM pricing across multiple AI providers (OpenAI, Anthropic, Google,
DeepSeek, Meta, Mistral AI, xAI, Cohere, Qwen, etc.) and updates the "### Models Prices"
section in README.md (replacing the "<<fill table>>" placeholder or existing table).

Usage:
    python update_model_prices.py              # Updates README.md with curated models
    python update_model_prices.py --all        # Includes all available models
    python update_model_prices.py --dry-run    # Print table to stdout without modifying file
    python update_model_prices.py --companies openai,anthropic,google  # Filter companies
    python update_model_prices.py --sort-by input_price                # Sort by price
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# Supported companies and display formatting
PROVIDER_MAPPING = {
    'openai': {'name': 'OpenAI', 'aliases': ['openai']},
    'anthropic': {'name': 'Anthropic', 'aliases': ['anthropic']},
    'google': {'name': 'Google', 'aliases': ['google', 'google-ai', 'vertex_ai']},
    'deepseek': {'name': 'DeepSeek', 'aliases': ['deepseek']},
    'meta-llama': {'name': 'Meta', 'aliases': ['meta', 'meta-llama']},
    'mistralai': {'name': 'Mistral AI', 'aliases': ['mistral', 'mistralai']},
    'x-ai': {'name': 'xAI', 'aliases': ['x-ai', 'xai', 'grok']},
    'cohere': {'name': 'Cohere', 'aliases': ['cohere']},
    'qwen': {'name': 'Qwen', 'aliases': ['qwen', 'alibaba']}
}

# Curated popular / flagship models per provider for cost comparison
CURATED_MODELS = [
    # OpenAI
    ('openai/gpt-4o', 'Flagship multimodal & vision'),
    ('openai/gpt-4o-mini', 'High-efficiency fast tier'),
    ('openai/o3', 'Advanced reasoning & complex tasks'),
    ('openai/gpt-4.1', 'High-capability general purpose'),
    ('openai/gpt-4.1-mini', 'Affordable general purpose'),
    # Anthropic
    ('anthropic/claude-opus-5', 'Top-tier deep reasoning'),
    ('anthropic/claude-sonnet-5', 'Balanced intelligence & coding'),
    ('anthropic/claude-haiku-5.5', 'Ultra-fast & economical'),
    # Google
    ('google/gemini-2.5-pro', 'Flagship reasoning & 1M context'),
    ('google/gemini-2.5-flash', 'High-speed multimodal workhorse'),
    ('google/gemini-2.5-flash-lite', 'Ultra low-cost & high throughput'),
    # DeepSeek
    ('deepseek/deepseek-chat', 'High-performance general open weights'),
    ('deepseek/deepseek-r1-0528', 'Advanced reasoning & math/code'),
    ('deepseek/deepseek-v4.1-flash', 'High-speed budget tier'),
    # Meta
    ('meta-llama/llama-3.3-70b-instruct', 'Flagship open weights (70B)'),
    ('meta-llama/llama-3.1-70b-instruct', 'High-capability open weights (70B)'),
    ('meta-llama/llama-3.1-8b-instruct', 'Lightweight low-latency open weights (8B)'),
    # Mistral AI
    ('mistralai/mistral-large', 'Flagship multilingual reasoning'),
    ('mistralai/mistral-small-3.2-24b-instruct', 'Efficient enterprise tier'),
    ('mistralai/codestral-2508', 'Code generation specialist'),
    # xAI
    ('x-ai/grok-4.7', 'Flagship reasoning & 500k context'),
    ('x-ai/grok-4.5', 'High-performance reasoning'),
    # Cohere
    ('cohere/command-r-plus-08-2024', 'Enterprise RAG flagship'),
    ('cohere/command-r-08-2024', 'Cost-effective enterprise RAG'),
    ('cohere/command-a-plus', 'Multimodal enterprise tier'),
    # Qwen
    ('qwen/qwen-2.5-coder-32b-instruct', 'Open-weight code specialist (32B)'),
    ('qwen/qwen-2.5-72b-instruct', 'Flagship open-weight general (72B)'),
    ('qwen/qwen-2.5-7b-instruct', 'Fast & lightweight open weights (7B)')
]

# Static fallback in case all external APIs are unreachable (e.g. offline mode)
OFFLINE_FALLBACK = [
    {'provider': 'OpenAI', 'model': 'GPT-4o', 'input_price': 2.50, 'output_price': 10.00, 'context': 128000, 'note': 'Flagship multimodal & vision'},
    {'provider': 'OpenAI', 'model': 'GPT-4o mini', 'input_price': 0.15, 'output_price': 0.60, 'context': 128000, 'note': 'High-efficiency fast tier'},
    {'provider': 'OpenAI', 'model': 'o3', 'input_price': 2.00, 'output_price': 8.00, 'context': 200000, 'note': 'Advanced reasoning & complex tasks'},
    {'provider': 'Anthropic', 'model': 'Claude Opus 5', 'input_price': 5.00, 'output_price': 25.00, 'context': 1000000, 'note': 'Top-tier deep reasoning'},
    {'provider': 'Anthropic', 'model': 'Claude Sonnet 5', 'input_price': 2.00, 'output_price': 10.00, 'context': 1000000, 'note': 'Balanced intelligence & coding'},
    {'provider': 'Anthropic', 'model': 'Claude Haiku 5.5', 'input_price': 0.10, 'output_price': 0.50, 'context': 1000000, 'note': 'Ultra-fast & economical'},
    {'provider': 'Google', 'model': 'Gemini 2.5 Pro', 'input_price': 1.25, 'output_price': 10.00, 'context': 1048576, 'note': 'Flagship reasoning & 1M context'},
    {'provider': 'Google', 'model': 'Gemini 2.5 Flash', 'input_price': 0.30, 'output_price': 2.50, 'context': 1048576, 'note': 'High-speed multimodal workhorse'},
    {'provider': 'Google', 'model': 'Gemini 2.5 Flash Lite', 'input_price': 0.10, 'output_price': 0.40, 'context': 1048576, 'note': 'Ultra low-cost & high throughput'},
    {'provider': 'DeepSeek', 'model': 'DeepSeek V3', 'input_price': 0.32, 'output_price': 0.89, 'context': 163840, 'note': 'High-performance general open weights'},
    {'provider': 'DeepSeek', 'model': 'DeepSeek R1', 'input_price': 0.50, 'output_price': 2.15, 'context': 163840, 'note': 'Advanced reasoning & math/code'},
    {'provider': 'Meta', 'model': 'Llama 3.3 70B Instruct', 'input_price': 0.71, 'output_price': 0.71, 'context': 131072, 'note': 'Flagship open weights (70B)'},
    {'provider': 'Meta', 'model': 'Llama 3.1 8B Instruct', 'input_price': 0.02, 'output_price': 0.04, 'context': 131072, 'note': 'Lightweight low-latency open weights (8B)'},
    {'provider': 'Mistral AI', 'model': 'Mistral Large', 'input_price': 2.00, 'output_price': 6.00, 'context': 128000, 'note': 'Flagship multilingual reasoning'},
    {'provider': 'Mistral AI', 'model': 'Codestral', 'input_price': 0.30, 'output_price': 0.90, 'context': 256000, 'note': 'Code generation specialist'},
    {'provider': 'xAI', 'model': 'Grok 4.7', 'input_price': 2.00, 'output_price': 6.00, 'context': 500000, 'note': 'Flagship reasoning & 500k context'},
    {'provider': 'Cohere', 'model': 'Command R+', 'input_price': 2.50, 'output_price': 10.00, 'context': 128000, 'note': 'Enterprise RAG flagship'},
    {'provider': 'Qwen', 'model': 'Qwen 2.5 Coder 32B', 'input_price': 0.66, 'output_price': 1.00, 'context': 32768, 'note': 'Open-weight code specialist (32B)'}
]


def fetch_openrouter_models(timeout: int = 10):
    """Fetch live model catalog and pricing from OpenRouter API."""
    url = "https://openrouter.ai/api/v1/models"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "CostOptimization/1.0 (pricing-updater)"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        if response.status == 200:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("data", [])
    return []


def infer_tier(model_id: str, prompt_cost: float, comp_cost: float) -> str:
    """Infer a concise capability/tier description from model properties."""
    mid = model_id.lower()
    if any(k in mid for k in ['r1', 'o1', 'o3', 'reason']):
        return 'Advanced Reasoning'
    elif any(k in mid for k in ['coder', 'codex', 'code']):
        return 'Code Specialist'
    elif any(k in mid for k in ['image', 'vision', 'omni']):
        return 'Multimodal / Vision'
    elif prompt_cost >= 5.0 or comp_cost >= 20.0:
        return 'Premium Flagship'
    elif prompt_cost >= 1.5:
        return 'High Intelligence / Balanced'
    elif prompt_cost <= 0.15:
        return 'Ultra-Low Cost / Fast'
    elif prompt_cost <= 0.60:
        return 'Budget / Efficient'
    return 'Standard General Purpose'


def clean_model_name(raw_name: str, model_id: str) -> str:
    """Clean model name to be human-friendly."""
    name = raw_name
    if ':' in name:
        name = name.split(':', 1)[1].strip()
    return name


def format_context(context_tokens: int) -> str:
    """Format token count cleanly (e.g., 128k, 1M, 2M)."""
    if not context_tokens:
        return "-"
    if context_tokens >= 1_000_000:
        val = context_tokens / 1_000_000
        return f"{val:.1f}M".replace(".0M", "M")
    return f"{context_tokens // 1000}k"


def format_price(price: float) -> str:
    """Format price per 1M tokens."""
    if price == 0:
        return "$0.00"
    if price < 0.01:
        return f"${price:.4f}"
    return f"${price:.2f}"


def build_models_list(raw_models: list, all_models: bool = False, limit_per_company: int = None, selected_companies: list = None) -> list:
    """Process raw API models into normalized records."""
    if not raw_models:
        return OFFLINE_FALLBACK

    model_dict = {m['id']: m for m in raw_models}
    results = []

    # Filter companies if requested
    active_providers = {}
    for prov_key, info in PROVIDER_MAPPING.items():
        if selected_companies:
            if any(alias in selected_companies for alias in info['aliases']):
                active_providers[prov_key] = info['name']
        else:
            active_providers[prov_key] = info['name']

    if not all_models:
        # Curated mode
        for mid, note in CURATED_MODELS:
            prov_key = mid.split('/')[0]
            if prov_key not in active_providers:
                continue
            m = model_dict.get(mid)
            if not m:
                continue
            p_in = float(m.get('pricing', {}).get('prompt', 0)) * 1_000_000
            p_out = float(m.get('pricing', {}).get('completion', 0)) * 1_000_000
            results.append({
                'provider': active_providers[prov_key],
                'model': clean_model_name(m.get('name', mid), mid),
                'input_price': p_in,
                'output_price': p_out,
                'context': m.get('context_length', 0),
                'note': note,
                'id': mid
            })
    else:
        # Full mode across active providers
        by_company = {}
        for m in raw_models:
            mid = m.get('id', '')
            # Ignore batch variations and test models to keep table clean
            if ':batch' in mid or ':free' in mid:
                continue
            prov_key = mid.split('/')[0]
            if prov_key not in active_providers:
                continue

            p_in = float(m.get('pricing', {}).get('prompt', 0)) * 1_000_000
            p_out = float(m.get('pricing', {}).get('completion', 0)) * 1_000_000
            tier = infer_tier(mid, p_in, p_out)

            record = {
                'provider': active_providers[prov_key],
                'model': clean_model_name(m.get('name', mid), mid),
                'input_price': p_in,
                'output_price': p_out,
                'context': m.get('context_length', 0),
                'note': tier,
                'id': mid
            }
            by_company.setdefault(active_providers[prov_key], []).append(record)

        for comp, mlist in by_company.items():
            if limit_per_company:
                results.extend(mlist[:limit_per_company])
            else:
                results.extend(mlist)

    return results


def sort_models(models: list, sort_by: str) -> list:
    """Sort models by chosen attribute."""
    if sort_by == 'input_price':
        return sorted(models, key=lambda x: (x['input_price'], x['output_price']))
    elif sort_by == 'output_price':
        return sorted(models, key=lambda x: (x['output_price'], x['input_price']))
    elif sort_by == 'context':
        return sorted(models, key=lambda x: x['context'], reverse=True)
    elif sort_by == 'model':
        return sorted(models, key=lambda x: x['model'].lower())
    else:
        # Default: by provider, then input price
        return sorted(models, key=lambda x: (x['provider'], x['input_price']))


def generate_markdown_table(models: list) -> str:
    """Generate the markdown table string with metadata and insights."""
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Find key highlights for cost optimization
    cheapest_input = min(models, key=lambda x: x['input_price'] if x['input_price'] > 0 else 999)
    cheapest_reasoning = min(
        [m for m in models if any(k in m['note'].lower() for k in ['reasoning', 'math'])],
        key=lambda x: x['input_price'],
        default=None
    )
    max_context = max(models, key=lambda x: x['context'])

    lines = []
    lines.append("<!-- MODEL_PRICES_START -->")
    lines.append(f"> [!NOTE]")
    lines.append(f"> **Prices updated:** {now_utc} | **Unit:** USD per 1 Million tokens ($/1M tokens).")
    lines.append(f"> Source: Real-time provider pricing aggregated via OpenRouter API.")

    lines.append("")
    lines.append("| Provider | Model | Input ($/1M) | Output ($/1M) | Context | Tier / Key Capabilities |")
    lines.append("| :--- | :--- | :---: | :---: | :---: | :--- |")

    for m in models:
        lines.append(
            f"| **{m['provider']}** | {m['model']} | "
            f"{format_price(m['input_price'])} | {format_price(m['output_price'])} | "
            f"{format_context(m['context'])} | {m['note']} |"
        )

    lines.append("")
    lines.append("**Quick Cost Insights:**")
    lines.append(f"- **Lowest input cost:** `{cheapest_input['model']}` ({cheapest_input['provider']}) at {format_price(cheapest_input['input_price'])} / 1M tokens.")
    if cheapest_reasoning:
        lines.append(f"- **Most affordable reasoning:** `{cheapest_reasoning['model']}` ({cheapest_reasoning['provider']}) at {format_price(cheapest_reasoning['input_price'])} / 1M tokens.")
    lines.append(f"- **Largest context window:** `{max_context['model']}` ({max_context['provider']}) with {format_context(max_context['context'])} tokens.")
    lines.append("<!-- MODEL_PRICES_END -->")

    return "\n".join(lines)


def update_readme(readme_path: Path, new_table_md: str) -> bool:
    """Update README.md at the <<fill table>> placeholder or between markers."""
    if not readme_path.exists():
        print(f"Error: Target file '{readme_path}' not found.", file=sys.stderr)
        return False

    content = readme_path.read_text(encoding="utf-8")

    # Strategy 1: Replace existing comment markers if already present
    marker_pattern = re.compile(
        r"<!-- MODEL_PRICES_START -->.*?<!-- MODEL_PRICES_END -->",
        re.DOTALL
    )
    if marker_pattern.search(content):
        updated_content = marker_pattern.sub(new_table_md, content)
        readme_path.write_text(updated_content, encoding="utf-8")
        return True

    # Strategy 2: Replace <<fill table>> placeholder
    if "<<fill table>>" in content:
        updated_content = content.replace("<<fill table>>", new_table_md)
        readme_path.write_text(updated_content, encoding="utf-8")
        return True

    # Strategy 3: Find "### Models Prices" section and replace up to next header or end
    section_pattern = re.compile(
        r"(###\s+Models\s+Prices\s*\n)(.*?)(?=(\n###|\n##|\Z))",
        re.DOTALL | re.IGNORECASE
    )
    if section_pattern.search(content):
        updated_content = section_pattern.sub(rf"\1\n{new_table_md}\n\n", content)
        readme_path.write_text(updated_content, encoding="utf-8")
        return True

    # Fallback: Append to end of file
    updated_content = content.rstrip() + f"\n\n### Models Prices\n\n{new_table_md}\n"
    readme_path.write_text(updated_content, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Fetch multi-company LLM pricing and update README.md"
    )
    parser.add_argument(
        "--file", "-f",
        default="README.md",
        help="Path to README.md (default: README.md)"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Include all available models from selected providers (not just curated)"
    )
    parser.add_argument(
        "--companies", "-c",
        help="Comma-separated list of companies (e.g. openai,anthropic,google,deepseek,meta,mistral,xai,cohere,qwen)"
    )
    parser.add_argument(
        "--sort-by", "-s",
        choices=['provider', 'input_price', 'output_price', 'context', 'model'],
        default='provider',
        help="Field to sort models by (default: provider)"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=None,
        help="Max models per company (useful with --all)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Output markdown table to stdout without modifying README.md"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw data as JSON to stdout"
    )

    args = parser.parse_args()

    # Parse companies filter
    selected_companies = None
    if args.companies:
        selected_companies = [c.strip().lower() for c in args.companies.split(',')]

    print("Fetching latest model pricing data...")
    raw_models = []
    try:
        raw_models = fetch_openrouter_models(timeout=10)
        print(f"Successfully retrieved {len(raw_models)} models from OpenRouter API.")
    except Exception as e:
        print(f"Warning: Could not fetch from OpenRouter API ({e}). Falling back to cached data.")

    models = build_models_list(
        raw_models,
        all_models=args.all,
        limit_per_company=args.limit,
        selected_companies=selected_companies
    )
    models = sort_models(models, args.sort_by)

    if args.json:
        print(json.dumps(models, indent=2))
        return 0

    table_md = generate_markdown_table(models)

    if args.dry_run:
        print("\n--- Generated Markdown Table ---\n")
        print(table_md)
        return 0

    readme_path = Path(args.file)
    success = update_readme(readme_path, table_md)
    if success:
        print(f"\n[OK] Successfully updated '{readme_path}' with pricing for {len(models)} models across multiple providers!")
    else:
        print(f"\n[FAILED] Could not update '{readme_path}'.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
