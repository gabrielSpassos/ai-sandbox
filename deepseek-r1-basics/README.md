# DeepSeek R1 Basics

> https://arxiv.org/abs/2501.12948

🎯 Goal of your first POC

- Run a DeepSeek-R1 (small version) locally.
- Ask it simple reasoning/math/logic questions.
- See both the chain of thought (<think> block) and the final answer.
- Compare it with a non-R1 model (like Llama or GPT-style) to feel the difference.

* Install Ollama
```
curl -fsSL https://ollama.com/install.sh | sh
```

```
ollama pull deepseek-r1:1.5b
ollama run deepseek-r1:1.5b
```

