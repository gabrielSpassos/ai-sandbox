import torch.nn.functional as F
import torch.optim as optim


def train_teacher(model, loader, device, epochs, lr):
    model.train()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        total_loss = 0

        for data, target in loader:
            data, target = data.to(device), target.to(device)

            optimizer.zero_grad()
            output = model(data)
            loss = F.cross_entropy(output, target)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Teacher epoch {epoch+1}, loss={total_loss:.3f}")
