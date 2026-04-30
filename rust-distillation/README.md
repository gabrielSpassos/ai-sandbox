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