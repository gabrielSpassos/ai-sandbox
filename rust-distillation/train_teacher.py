import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms

device = "cpu"

train_loader = torch.utils.data.DataLoader(
    datasets.MNIST(
        ".", train=True, download=True,
        transform=transforms.ToTensor()
    ),
    batch_size=64,
    shuffle=True
)

class Teacher(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 3)
        self.conv2 = nn.Conv2d(32, 64, 3)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        # MUST be [N, 1, 28, 28]
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2)
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        return self.fc2(x)

model = Teacher().to(device)
opt = torch.optim.Adam(model.parameters(), lr=1e-3)

# ---- TRAIN ----
for epoch in range(3):
    for x, y in train_loader:
        x, y = x.to(device), y.to(device)

        # 🚫 DO NOT reshape x
        out = model(x)

        loss = F.cross_entropy(out, y)

        opt.zero_grad()
        loss.backward()
        opt.step()

model.eval()

# ---- TRACE (CRITICAL) ----
example = torch.randn(1, 1, 28, 28)  # ✅ 4D ONLY

# sanity check
print("Sanity output shape:", model(example).shape)

traced = torch.jit.trace(model, example)
torch.jit.save(traced, "teacher.pt")
