import pandas as pd
from src.data_loader import load_data

def test_load_data(tmp_path):
    file_path = tmp_path / "sample.csv"
    df = pd.DataFrame({"text": ["hello world", "", None, "another doc"]})
    df.to_csv(file_path, index=False)

    loaded = load_data(str(file_path), "text")
    assert len(loaded) == 2
    assert loaded.iloc[0]["text"] == "hello world"
    assert loaded.iloc[1]["text"] == "another doc"
