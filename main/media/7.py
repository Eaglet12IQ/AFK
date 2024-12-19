import re

# Алфавит для русского языка, 32 символа
ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def preprocess_text(text):
    # Привести к нижнему регистру и удалить все, кроме букв и пробелов
    text = text.lower()
    text = re.sub(r'[^а-яё ]', '', text)
    return text


def caesar_cipher(text, shift, mode='encrypt'):
    result = ''
    shift = shift % len(ALPHABET)

    if mode == 'decrypt':
        shift = -shift

    for char in text:
        if char in ALPHABET:
            index = ALPHABET.index(char)
            new_index = (index + shift) % len(ALPHABET)
            result += ALPHABET[new_index]
        else:
            result += char

    return result


def vigenere_cipher(text, key, mode='encrypt'):
    key = preprocess_text(key)
    result = ''
    key_length = len(key)

    for i, char in enumerate(text):
        if char in ALPHABET:
            text_index = ALPHABET.index(char)
            key_index = ALPHABET.index(key[i % key_length])

            if mode == 'encrypt':
                new_index = (text_index + key_index) % len(ALPHABET)
            elif mode == 'decrypt':
                new_index = (text_index - key_index) % len(ALPHABET)

            result += ALPHABET[new_index]
        else:
            result += char

    return result


# Пример выполнения
text = "Пример сообщения для шифрования"
processed_text = preprocess_text(text)

# Шифр простой замены (Цезаря)
shift = int(input("Введите сдвиг для шифра Цезаря: "))
encrypted_text_caesar = caesar_cipher(processed_text, shift)
decrypted_text_caesar = caesar_cipher(encrypted_text_caesar, shift, mode='decrypt')

# Шифр Виженера
key = input("Введите ключ для шифра Виженера: ")
encrypted_text_vigenere = vigenere_cipher(processed_text, key)
decrypted_text_vigenere = vigenere_cipher(encrypted_text_vigenere, key, mode='decrypt')

# Вывод результатов
print(f"Исходный текст: {processed_text}")
print(f"Зашифрованный текст (Цезарь): {encrypted_text_caesar}")
print(f"Расшифрованный текст (Цезарь): {decrypted_text_caesar}")
print(f"Зашифрованный текст (Виженер): {encrypted_text_vigenere}")
print(f"Расшифрованный текст (Виженер): {decrypted_text_vigenere}")