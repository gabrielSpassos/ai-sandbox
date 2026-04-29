import torch
import torch.nn as nn
import torch.nn.functional as F

class Teacher(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(28*28, 256)
        self.fc2 = nn.Linear(256, 10)

    def forward(self, x):
        x = x.view(-1, 28*28)
        x = F.relu(self.fc1(x))
        return self.fc2(x)

model = Teacher()

# random weights (for now)
model.eval()

example = torch.randn(1, 1, 28, 28)
traced = torch.jit.trace(model, example)

torch.jit.save(traced, "teacher.pt")
