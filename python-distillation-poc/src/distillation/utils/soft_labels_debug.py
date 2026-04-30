def debug_soft_vs_hard(teacher_logits, soft_teacher, labels, max_samples=3):
    preds = teacher_logits.argmax(dim=1)

    print("\n=== Soft vs Hard Labels Debug ===")

    for i in range(min(max_samples, len(labels))):
        print(f"\nSample {i}")
        print(f"Hard label: {labels[i].item()}")
        print(f"Teacher prediction: {preds[i].item()}")

        top_probs, top_indices = soft_teacher[i].topk(3)

        print("Top-3 soft probabilities:")
        for prob, idx in zip(top_probs, top_indices):
            print(f"  Class {idx.item()} → {prob.item():.4f}")
