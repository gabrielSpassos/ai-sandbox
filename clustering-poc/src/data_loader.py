import pandas as pd

def load_data(path: str, text_column: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' not found in {path}")
    df = df[[text_column]].dropna()
    df[text_column] = df[text_column].astype(str).str.strip()
    df = df[df[text_column] != ""].reset_index(drop=True)
    return df
