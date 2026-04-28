# LLM Distillation POC

## What is?

While training from diverse data and increasing the number of parameters produces powerful models, real-world application becomes challenging. Deploying larger and larger models to edge devices like mobile phones and smart devices becomes difficult because of their intensive computational requirements and costs. 

Process of transferring knowledge from a larger (often more complex) model (teacher) to a smaller, more efficient model (student)

Large and Small is a Meassure in terms of parameters

Concept of 2015, from paper Distilling the Knowledge in Neural Network

The goal is to maintain the smaller model performance as close possible to the teacher model, while reducing the computation resources.

Temperature:
    - today: 
        - llm creativity knob
            - high temperature means more surprising LLM outputs
    - Originally:
        - amplify dark knowledge by artifically increase the probabilities of the wrong lables 
## How it works?

1. Teacher model generate soft labels
   - Soft lables: 
        - teacher models outputs the probability distributions over possible answers
        - this allows studant model understand confidence levels rather than just right and wrong
        - dark knowlegde
            - knowlegde about what the input is not.
2. Besides train with soft labels, the studant models learns from the ground truth
3. These two training tecniques help the student capture the reasoning patterns of teacher
4. Student also can be fine-tuned on task specific data sets
    - helps to perform well in real word applications even if its much smaller than the teacher

## Why use LLM distillation (Pros)
1. Efficiency
    - smaller llms require less computational power, fits for edge devides or low latency applications
2. Cost savings
    - with efficiency has reduce resource consumption leads to lower inference in operational cost
3. Scalability 
    - with efficiency can scale up to more user to taks with less need of massive infrastrucute
4. Decoupling to train with bigger models but deploy with smaller and faster models

#### Pros
- Enables decoupling, meaning can use huge models for training and deploy 
- Smaller and faster
- Cheaper to deploy
- Often robust

## Challenges (Cons)

1. Information loss
    - the smaller model might not fully capture the nuances of the teacher
2. Ensure Generalization
    - if the student generalizes well across diverse taks or domains

#### Cons
- Requires that the teacher be a white box (access the probability distributions)
- Training pipeline becomes more complex and more expensive
- Some accuracy loss is common
- Requires a strong teacher model

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

#### Real Word cases

- DistillBERT
    - distilled from Bert, develop by Google
    - 40% smaller, 60% faster and 97% performance of Bert
- DistillGPT-2
    - Distilled from gpt2, from open AI
    - 35~40% smaller, 50% faster, and 95~97% performance of gpt2

## Resources

* youtube video: https://www.youtube.com/watch?v=h7DUpHPasME
* paper: https://arxiv.org/pdf/1503.02531

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
