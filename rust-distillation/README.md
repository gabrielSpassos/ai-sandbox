# Usage

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install numpy==1.26.4
pip install torch==2.2.0 torchvision==0.17.0 --index-url https://download.pytorch.org/whl/cpu
python train_teacher.py
mv teacher.pt models/
cargo clean
export LIBTORCH_USE_PYTORCH=1
export LIBTORCH_BYPASS_VERSION_CHECK=1
export LD_LIBRARY_PATH=$(python -c "import torch, os; print(os.path.join(os.path.dirname(torch.__file__), 'lib'))"):$LD_LIBRARY_PATH
cargo run
```

# Output

* alfa = 0.5
```
Knowledge Distillation!
Train dataset shape: [60000, 1, 28, 28]
Test dataset shape: [10000, 1, 28, 28]
Epoch 0
Epoch 0 avg loss: 3.1391 | accuracy: 90.24%
Epoch 1
Epoch 1 avg loss: 2.2236 | accuracy: 95.36%
Epoch 2
Epoch 2 avg loss: 2.0210 | accuracy: 96.77%
Epoch 3
Epoch 3 avg loss: 1.9203 | accuracy: 97.53%
Epoch 4
Epoch 4 avg loss: 1.8605 | accuracy: 98.08%
Test accuracy: 97.39%
```

* alfa - 1.0 (without destillation)
```
Train dataset shape: [60000, 1, 28, 28]
Test dataset shape: [10000, 1, 28, 28]
Epoch 0
Epoch 0 avg loss: 0.3115 | accuracy: 91.24%
Epoch 1
Epoch 1 avg loss: 0.1475 | accuracy: 95.63%
Epoch 2
Epoch 2 avg loss: 0.1033 | accuracy: 96.92%
Epoch 3
Epoch 3 avg loss: 0.0776 | accuracy: 97.70%
Epoch 4
Epoch 4 avg loss: 0.0600 | accuracy: 98.25%
Test accuracy: 96.79%
```