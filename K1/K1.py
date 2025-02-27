def preprocess(text, letters):
    original = []
    clean = []
    for c in text:
        original.append(c)
        lower_c = c.lower()
        if lower_c in letters:
            clean.append(lower_c)
    return original, clean

def find_key_length(text, max_len=30):
    best_len, best_ic = 1, 0
    for l in range(1, max_len+1):
        groups = [[] for _ in range(l)]
        for i, c in enumerate(text):
            groups[i % l].append(c)
        ic = sum(calculate_ic(g) for g in groups) / l
        if ic > best_ic:
            best_len, best_ic = l, ic
    return best_len

def calculate_ic(group):
    counts = {}
    for c in group:
        counts[c] = counts.get(c, 0) + 1
    n = len(group)
    if n < 2: return 0
    return sum(cnt*(cnt-1) for cnt in counts.values()) / (n*(n-1))

def find_key(text, key_len, freqs, letters):
    key = []
    letter_to_idx = {char: idx for idx, char in enumerate(letters)}
    for i in range(key_len):
        group = text[i::key_len]
        key.append(letters[best_shift(group, freqs, letters, letter_to_idx)])
    return ''.join(key)

def best_shift(group, freqs, letters, letter_to_idx):
    min_err = float('inf')
    best_shift = 0
    total_chars = len(letters)
    
    for shift in range(total_chars):
        error = 0.0
        freq_actual = [0.0] * total_chars
        total = len(group)
        if total == 0:
            continue
        
        for c in group:
            original_idx = (letter_to_idx[c] - shift) % total_chars
            freq_actual[original_idx] += 1.0 / total
        
        for j in range(total_chars):
            error += (freq_actual[j] - freqs[j]) ** 2
        
        if error < min_err:
            min_err = error
            best_shift = shift
    return best_shift

def decrypt(original, clean, key, letters):
    letter_to_idx = {char: idx for idx, char in enumerate(letters)}
    key_shifts = [letter_to_idx[c] for c in key]
    key_len = len(key)
    result = []
    clean_idx = 0
    
    for c in original:
        if c.lower() in letters:
            is_upper = c.isupper()
            current_char = c.lower()
            shift = key_shifts[clean_idx % key_len]
            original_idx = (letter_to_idx[current_char] - shift) % len(letters)
            decrypted_char = letters[original_idx]
            result.append(decrypted_char.upper() if is_upper else decrypted_char)
            clean_idx += 1
        else:
            result.append(c)
    return ''.join(result)

def main():
    expected_freq = [
        0.0801, 0.0159, 0.0454, 0.0165, 0.0296, 0.0845, 0.0040, 0.0073,
        0.0160, 0.0734, 0.0121, 0.0349, 0.0440, 0.0321, 0.0670, 0.1097,
        0.0281, 0.0473, 0.0547, 0.0626, 0.0262, 0.0026, 0.0097, 0.0048,
        0.0144, 0.0073, 0.0036, 0.0004, 0.0190, 0.0174, 0.0032, 0.0064,
        0.0201
    ]
    
    russian_letters = [
        'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м',
        'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ',
        'ы', 'ь', 'э', 'ю', 'я'
    ]

    with open('K1/original_text.txt', 'r', encoding='utf-8') as f:
        ciphertext = f.read()

    original, clean = preprocess(ciphertext, russian_letters)
    
    key_len = find_key_length(clean)
    print(f"Найдена длина ключа: {key_len}")

    key = find_key(clean, key_len, expected_freq, russian_letters)
    print(f"Предполагаемый ключ: {key}")

    decrypted = decrypt(original, clean, key, russian_letters)
    print("\nРасшифрованный текст сохранен в файл K1/decrypted_text.txt")

    with open('K1/decrypted_text.txt', 'w', encoding='utf-8') as f:
        f.write(decrypted)

if __name__ == "__main__":
    main()