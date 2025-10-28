name = "Babin Bid"
words = name.split()

for word in words:
    clean_word = word.replace('.', '').replace(',', '')
    print(f"Word: '{word}' -> '{clean_word}'")
    print(f"  Length >= 2: {len(clean_word) >= 2}")
    print(f"  All alpha or hyphen: {all(c.isalpha() or c == '-' for c in clean_word)}")
    print(f"  Starts with capital: {clean_word[0].isupper() if clean_word else False}")
    print()
