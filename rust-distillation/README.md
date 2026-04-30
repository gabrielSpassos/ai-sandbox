# Usage

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install torch==2.2.0
cargo clean
export LIBTORCH_USE_PYTORCH=1
export LIBTORCH_BYPASS_VERSION_CHECK=1
cargo run
```