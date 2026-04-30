import torch
import os

def save_soft_labels(batch_idx, soft_labels, labels, path="logs/soft_labels"):
    os.makedirs(path, exist_ok=True)

    file_path = os.path.join(path, f"batch_{batch_idx}.pt")

    torch.save({
        "soft_labels": soft_labels.cpu(),
        "hard_labels": labels.cpu()
    }, file_path)