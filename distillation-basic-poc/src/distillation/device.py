import torch


def get_device():
    # NVIDIA GeForce MX150 incompatible with latest PyTorch versions
    # return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device("cpu")
