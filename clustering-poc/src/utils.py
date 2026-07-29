from pathlib import Path

def ensure_output_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)
