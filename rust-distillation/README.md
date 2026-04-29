# Usage

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install torch==2.2.0 --index-url https://download.pytorch.org/whl/cpu
cargo clean
export LIBTORCH_USE_PYTORCH=1
export LIBTORCH_BYPASS_VERSION_CHECK=1
export LD_LIBRARY_PATH=$(python -c "import torch, os; print(os.path.join(os.path.dirname(torch.__file__), 'lib'))"):$LD_LIBRARY_PATH
cargo run
```