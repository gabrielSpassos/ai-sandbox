import torch
import torch.optim as optim
from .distillation_loss import distillation_loss


def train_student(student, teacher, loader, device, epochs, lr,
                  temperature, alpha):

    student.train()
    teacher.eval()

    optimizer = optim.Adam(student.parameters(), lr=lr)

    for epoch in range(epochs):
        total_loss = 0

        for data, target in loader:
            data, target = data.to(device), target.to(device)

            with torch.no_grad():
                teacher_logits = teacher(data)

            student_logits = student(data)

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
