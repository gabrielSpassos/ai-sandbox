from src.distillation.device import get_device
from src.distillation.data import get_dataloaders
from src.distillation.models.teacher import TeacherNet
from src.distillation.models.student import StudentNet
from src.distillation.training.train_teacher import train_teacher
from src.distillation.training.train_student import train_student
from src.distillation.evaluation.evaluate import evaluate
from src.distillation.config import *


def main():
    device = get_device()

    train_loader, test_loader = get_dataloaders(BATCH_SIZE)

    teacher = TeacherNet().to(device)
    student = StudentNet().to(device)

    print("Training teacher...")
    train_teacher(teacher, train_loader, device, EPOCHS_TEACHER, LR)

    print("\nTraining student with distillation...")
    train_student(
        student,
        teacher,
        train_loader,
        device,
        EPOCHS_STUDENT,
        LR,
        TEMPERATURE,
        ALPHA
    )

    print("\nEvaluation:")
    evaluate(teacher, test_loader, device, "Teacher")
    evaluate(student, test_loader, device, "Student")


if __name__ == "__main__":
    main()
