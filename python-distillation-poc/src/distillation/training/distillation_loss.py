import torch.nn.functional as F


def distillation_loss(student_logits, teacher_logits, labels,
                      temperature, alpha):

    soft_teacher = F.softmax(teacher_logits / temperature, dim=1)
    soft_student = F.log_softmax(student_logits / temperature, dim=1)

    soft_loss = F.kl_div(soft_student, soft_teacher, reduction="batchmean") * (temperature**2)
    hard_loss = F.cross_entropy(student_logits, labels)

    return alpha * soft_loss + (1 - alpha) * hard_loss
