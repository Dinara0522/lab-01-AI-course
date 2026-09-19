import tiktoken

from texts import KAZAKH_COMMON, KAZAKH_SPECIFIC


texts = {
    "Kazakh common letters": KAZAKH_COMMON,
    "Kazakh specific letters": KAZAKH_SPECIFIC,
}

tokenizers = {
    "o200k_base": tiktoken.get_encoding("o200k_base"),
    "cl100k_base": tiktoken.get_encoding("cl100k_base"),
}


print("=" * 72)
print("KAZAKH CHARACTER COMPARISON")
print("=" * 72)

for name, text in texts.items():
    chars = len(text)
    bytes_count = len(text.encode("utf-8"))
    bytes_per_char = bytes_count / chars

    print(f"\n{name}")
    print("-" * 72)
    print(f"Text: {text}")
    print(f"Characters: {chars}")
    print(f"UTF-8 bytes: {bytes_count}")
    print(f"Bytes per character: {bytes_per_char:.2f}")

    for tokenizer_name, tokenizer in tokenizers.items():
        tokens = len(tokenizer.encode(text))
        print(f"{tokenizer_name} tokens: {tokens}")