import torch

def evaluate(model, loader, device, name="Model"):
    model.eval()
    correct = 0

    with torch.no_grad():
        for data, target in loader:
            data, target = data.to(device), target.to(device)
            preds = model(data).argmax(dim=1)
            correct += (preds == target).sum().item()

    accuracy = 100.0 * correct / len(loader.dataset)
    print(f"{name} accuracy: {accuracy:.2f}%")
