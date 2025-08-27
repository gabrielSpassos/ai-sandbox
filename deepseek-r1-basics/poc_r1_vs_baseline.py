# poc_r1_vs_baseline.py
import subprocess
import json
import textwrap
import re

# --- Config ---
R1_MODEL = "deepseek-r1:1.5b"   # small reasoning model
BASELINE_MODEL = "qwen2.5:1.5b" # baseline non-reasoning model
QUESTIONS = [
    "What is 17 * 24?",
    #"If Alice has 3 apples and Bob gives her 5 more, how many apples does she have?",
    #"A train leaves at 3pm and travels for 2 hours. What time does it arrive?",
    #"If John is taller than Mary, and Mary is taller than Alex, who is the tallest?",
]

# --- Helper function to run Ollama models ---
def ask_ollama(model, prompt):
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("Error running ollama:", result.stderr)
        return ""
    return result.stdout.strip()


def extract_final_answer(text: str) -> str:
    # 1) Remove reasoning <think>…</think> blocks
    text_no_reasoning = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    # 2) Look for "Final Answer: ..."
    match = re.search(r"Final Answer[:\-]?\s*(.*)", text_no_reasoning, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # 3) Fallback: take last line of the output
    lines = [l.strip() for l in text_no_reasoning.splitlines() if l.strip()]
    return lines[-1] if lines else ""


# --- Run comparison ---
for q in QUESTIONS:
    print("="*80)
    print(f"❓ Question: {q}\n")

    r1_answer = ask_ollama(R1_MODEL, q)
    base_answer = ask_ollama(BASELINE_MODEL, q)

    print("🤖 DeepSeek-R1:")
    print(textwrap.indent(r1_answer, "  "))

    print("\n🧠 Extracted final answer from R1:")
    print("  ", extract_final_answer(r1_answer))

    print("\n🟢 Baseline (Qwen2.5):")
    print(textwrap.indent(base_answer, "  "))

    print("\n")
