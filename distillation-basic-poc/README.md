# AI Distillation Basic POC

## What is?

Machine Learning technique, where a *simplier, smaller model (studant)* is trained to replicate the behavior of a *larger, more complex model (teacher)*, studant learns from the *teacher’s predictions* which contains richer information (often called soft targets).

The target is *retain most of teacher model's performance while reducing size, latency, and compute cost*

## How it works?

1. Train or obtain a powerful teacher model (large neural network, ensemble, or foundation model).
2. Run data through the teacher to produce probability distributions or outputs.
3. Train a student model to match those outputs (not just the correct label).
4. Deploy the smaller student model.

## Pros
- Smaller and faster
- Cheaper to deploy
- Often robust

## Cons
- Some accuracy loss is common
- Requires a strong teacher model
- Training pipeline becomes more complex

## Code

## Use Case

1. Edge and mobile deployment
    
    Large models often cannot run efficiently on phones, IoT devices, or embedded systems.

    Examples:

        - On-device speech recognition
        - Camera vision models
        - Offline translation apps

2. Large Language Model optimization

    Organizations distill large foundation models into smaller domain-specific ones.

    Examples:

        - Customer support chatbot distilled from a large LLM
        - Internal knowledge assistant
        - Coding assistant tuned for a specific language stack

    Benefits:

        - Faster responses 
        - Lower infrastructure cost
        - Better control and specialization

3. Production inference cost reduction

    At scale, inference cost dominates training cost.

    Companies distill:

        - Recommendation models
        - Fraud detection systems
        - Ranking models

    Result: same behavior, cheaper compute.

4. Privacy-sensitive deployments

    A large centralized model can train a smaller local model that runs without sending data to servers.

    Used in:

        - Healthcare tools
        - Enterprise on-prem systems
        - Personal devices

5. Ensemble compression

    Multiple models combined into one compact model.

    Example:

        - Replace a 10-model ensemble with a single distilled network
        - Keeps ensemble performance but simpler architecture

6. Domain adaptation

    Distill general intelligence into a specialized model.

    Examples:

        - Legal document classifier
        - Medical imaging detector
        - Financial risk analyzer

    The teacher provides broad knowledge; the student becomes efficient and specialized.

## Run POC

* Configure venv
```bash
python3 -m venv .venv
source .venv/bin/activate
```

* Install dependencies
```bash
pip3 install -r requirements.txt
```

* Run application
```bash
python3 main.py
```

## Output

```
Training teacher...
Teacher epoch 1, loss=190.393
Teacher epoch 2, loss=80.732
Teacher epoch 3, loss=56.475
Teacher epoch 4, loss=43.602
Teacher epoch 5, loss=34.902

Training student with distillation...
Student epoch 1, loss=2006.872
Student epoch 2, loss=558.022
Student epoch 3, loss=352.763
Student epoch 4, loss=269.218
Student epoch 5, loss=225.723
Student epoch 6, loss=198.993
Student epoch 7, loss=181.262
Student epoch 8, loss=166.299
Student epoch 9, loss=156.724
Student epoch 10, loss=148.099
Student epoch 11, loss=140.783
Student epoch 12, loss=135.527
Student epoch 13, loss=130.434
Student epoch 14, loss=126.409
Student epoch 15, loss=123.616
Student epoch 16, loss=120.076
Student epoch 17, loss=117.515
Student epoch 18, loss=115.142
Student epoch 19, loss=112.097
Student epoch 20, loss=111.278

Evaluation:

Teacher evaluation:
Accuracy: 97.69%
Parameters: 535,818
Model size: 2.15 MB
Latency: 0.3167 ms/sample

Student evaluation:
Accuracy: 97.46%
Parameters: 101,770
Model size: 0.41 MB
Latency: 0.2535 ms/sample
```
