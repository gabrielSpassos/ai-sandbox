from src.config import Config

def test_config_defaults():
    config = Config()
    assert config.input_path == "data/sample.csv"
    assert config.text_column == "text"
    assert config.output_dir == "output"
    assert config.top_n_words == 10
