from src.preprocessing import clean_text, preprocess_texts

def test_clean_text():
    text = "Hello!!! Visit https://example.com now."
    cleaned = clean_text(text)
    assert "http" not in cleaned
    assert "!" not in cleaned
    assert cleaned == "hello visit now"

def test_preprocess_texts():
    texts = ["Hello World!", "Second TEXT."]
    cleaned = preprocess_texts(texts)
    assert cleaned == ["hello world", "second text"]
