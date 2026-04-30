import torch
import torch.optim as optim
import torch.nn.functional as F

from .distillation_loss import distillation_loss
from src.distillation.utils.soft_labels_logger import save_soft_labels
from src.distillation.utils.soft_labels_debug import debug_soft_vs_hard
from src.distillation.utils.visualization import plot_soft_label


def train_student(student, teacher, loader, device, epochs, lr,
                  temperature, alpha):

    student.train()
    teacher.eval()

    optimizer = optim.Adam(student.parameters(), lr=lr)

    for epoch in range(epochs):
        total_loss = 0

        for batch_idx, (data, target) in enumerate(loader):
            data, target = data.to(device), target.to(device)

            with torch.no_grad():
                teacher_logits = teacher(data)

            student_logits = student(data)

            # Compute soft labels
            soft_teacher = F.softmax(teacher_logits / temperature, dim=1)

            # Save soft labels
            if epoch == 0 and batch_idx < 5:
                save_soft_labels(batch_idx, soft_teacher, target)

            # Soft vs Hard Label comparison
            if epoch == 0 and batch_idx == 0:
                debug_soft_vs_hard(teacher_logits, soft_teacher, target)

            # Visualization
            if epoch == 0 and batch_idx == 0:
                plot_soft_label(
                    soft_teacher[0].cpu().numpy(),
                    filename=f"epoch_{epoch}_batch_{batch_idx}.png"
                )

            # Distillation loss
            loss = distillation_loss(
                student_logits,
                teacher_logits,
                target,
                temperature,
                alpha
            )

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Student epoch {epoch+1}, loss={total_loss:.3f}")