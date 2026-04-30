import torch

data = torch.load("logs/soft_labels/batch_0.pt")

soft = data["soft_labels"]
hard = data["hard_labels"]

print("Soft label example:", soft[0])
print("Hard label:", hard[0])
