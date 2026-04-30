import matplotlib.pyplot as plt
import os

def plot_soft_label(probs, title="Soft Label Distribution", save_path="logs/plots", filename="soft_label.png"):
    os.makedirs(save_path, exist_ok=True)

    file_path = os.path.join(save_path, filename)

    plt.figure()
    plt.bar(range(len(probs)), probs)
    plt.title(title)
    plt.xlabel("Class")
    plt.ylabel("Probability")

    plt.savefig(file_path)
    plt.close()

    print(f"[INFO] Plot saved to {file_path}")