import torch
import time
import os
import tempfile


def get_model_size_mb(model):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        torch.save(model.state_dict(), tmp.name)
        size_mb = os.path.getsize(tmp.name) / 1e6
    os.remove(tmp.name)
    return size_mb


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def evaluate(model, loader, device, name="Model"):
    model.eval()
    correct = 0
    total_samples = 0

    start_time = time.perf_counter()

    with torch.no_grad():
        for data, target in loader:
            data, target = data.to(device), target.to(device)

            outputs = model(data)
            preds = outputs.argmax(dim=1)

            correct += (preds == target).sum().item()
            total_samples += target.size(0)

    end_time = time.perf_counter()

    # Accuracy
    accuracy = 100.0 * correct / total_samples

    # Latency
    total_time = end_time - start_time
    latency_per_sample = total_time / total_samples * 1000  # ms

    # Model size
    model_size = get_model_size_mb(model)

    # Parameter count
    params = count_parameters(model)

    print(f"\n{name} evaluation:")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Parameters: {params:,}")
    print(f"Model size: {model_size:.2f} MB")
    print(f"Latency: {latency_per_sample:.4f} ms/sample")