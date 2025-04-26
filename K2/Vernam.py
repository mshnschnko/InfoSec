import base64
import re

# def break_vernam(c1_b64, c2_b64):
#     ct1 = base64.b64decode(c1_b64)
#     ct2 = base64.b64decode(c2_b64)
    
#     min_len = min(len(ct1), len(ct2))
#     ct1 = ct1[:min_len]
#     ct2 = ct2[:min_len]
    
#     xor_p1p2 = bytes([a ^ b for a, b in zip(ct1, ct2)])
    
#     p1_guess = []
#     p2_guess = []
    
#     for xor_byte in xor_p1p2:
#         p2_char = xor_byte ^ 0x20
#         p2_valid = 32 <= p2_char <= 126
        
#         p1_char = xor_byte ^ 0x20
#         p1_valid = 32 <= p1_char <= 126
        
#         if p2_valid and p1_valid:
#             p1_guess.append(f'{chr(p1_char)}/?')
#             p2_guess.append(f'{chr(p2_char)}/?')
#         elif p2_valid:
#             p1_guess.append(' ')
#             p2_guess.append(chr(p2_char))
#         elif p1_valid:
#             p1_guess.append(chr(p1_char))
#             p2_guess.append(' ')
#         else:
#             p1_guess.append('?')
#             p2_guess.append('?')
    
#     return (''.join(p1_guess), ''.join(p2_guess))

import base64
import re
from collections import defaultdict

CHAR_WEIGHTS = {
    ' ': 10,
    'e': 5, 't': 5, 'a': 5, 'o': 5, 'i': 5, 'n': 5,
    'о': 5, 'а': 5, 'е': 5, 'и': 5, 'н': 5, 'т': 5,
    '.': 3, ',': 3, '?': 2, '!': 2,
    '\n': 2, ':': 2, ';': 2, '-': 2
}

def break_vernam(c1_b64, c2_b64):
    ct1 = base64.b64decode(c1_b64)
    ct2 = base64.b64decode(c2_b64)
    
    min_len = min(len(ct1), len(ct2))
    ct1, ct2 = ct1[:min_len], ct2[:min_len]
    
    xor_p1p2 = bytes(a ^ b for a, b in zip(ct1, ct2))
    
    p1_guess = []
    p2_guess = []
    
    for xor_byte in xor_p1p2:
        best_p1 = ('?', 0)
        best_p2 = ('?', 0)
        
        for code in range(256):
            try:
                for encoding in ['utf-8', 'cp1251']:
                    p2_char = bytes([code ^ xor_byte])
                    p2_char_decoded = p2_char.decode(encoding, errors='replace')
                    p2_weight = CHAR_WEIGHTS.get(p2_char_decoded, 0.1)
                    
                    if p2_weight > best_p2[1]:
                        best_p2 = (p2_char_decoded, p2_weight)
                    
                    p1_char = bytes([xor_byte ^ code])
                    p1_char_decoded = p1_char.decode(encoding, errors='replace')
                    p1_weight = CHAR_WEIGHTS.get(p1_char_decoded, 0.1)
                    
                    if p1_weight > best_p1[1]:
                        best_p1 = (p1_char_decoded, p1_weight)
                        
            except Exception:
                continue
        
        p1_guess.append(best_p1[0])
        p2_guess.append(best_p2[0])
    
    return (''.join(p1_guess), ''.join(p2_guess))


def main():
    ciphertext1_b64, ciphertext2_b64 = read_vernam_ciphers('2texts.txt')
    p1, p2 = break_vernam(ciphertext1_b64, ciphertext2_b64)

    print("Предполагаемый текст 1:")
    print(p1)
    print("\nПредполагаемый текст 2:")
    print(p2)

def read_vernam_ciphers(filename):
    ciphers = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
        
        for i in range(0, len(lines), 2):
            if not re.match(r'^Шифр \d+ \(base64\):$', lines[i]):
                raise ValueError(f"Некорректный заголовок в строке {i+1}")
            
            data_line = lines[i+1]
            if not (data_line.startswith('b\'') and data_line.endswith('\'')):
                raise ValueError(f"Некорректный формат данных в строке {i+2}")
            
            ciphers.append(data_line[2:-1])
    
    return ciphers

if __name__ == "__main__":
    main()
