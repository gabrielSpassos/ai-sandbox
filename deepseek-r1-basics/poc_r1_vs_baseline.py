# poc_r1_vs_baseline.py
import subprocess
import json
import textwrap

# --- Config ---
R1_MODEL = "deepseek-r1:1.5b"   # small reasoning model
BASELINE_MODEL = "qwen2.5:1.5b" # baseline non-reasoning model
QUESTIONS = [
    "What is 17 * 24?",
    "If Alice has 3 apples and Bob gives her 5 more, how many apples does she have?",
    "A train leaves at 3pm and travels for 2 hours. What time does it arrive?",
    "If John is taller than Mary, and Mary is taller than Alex, who is the tallest?",
]

# --- Helper function to run Ollama models ---
def ask_ollama(model, prompt):
    result = subprocess.run(
        ["ollama", "run", model, "--json"],
        input=prompt.encode(),
        capture_output=True,
        text=True
    )
    outputs = []
    for line in result.stdout.splitlines():
        try:
            data = json.loads(line)
            if "response" in data:
                outputs.append(data["response"])
        except json.JSONDecodeError:
            pass
    return "".join(outputs).strip()

# --- Run comparison ---
for q in QUESTIONS:
    print("="*80)
    print(f"❓ Question: {q}\n")

    r1_answer = ask_ollama(R1_MODEL, q)
    base_answer = ask_ollama(BASELINE_MODEL, q)

    print("🤖 DeepSeek-R1:")
    print(textwrap.indent(r1_answer, "  "))

    print("\n🟢 Baseline (Qwen2.5):")
    print(textwrap.indent(base_answer, "  "))

    print("\n")
