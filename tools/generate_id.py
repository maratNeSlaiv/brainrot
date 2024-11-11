import hashlib
import secrets

def generate_random_hash(length=16):
    # Генерируем случайную строку
    random_string = secrets.token_hex(8)  # Создаем 16-символьную строку
    # Хэшируем строку
    hash_object = hashlib.sha256(random_string.encode())
    # Преобразуем хэш в шестнадцатеричную строку и обрезаем до нужной длины
    hash_hex = hash_object.hexdigest()[:length]
    return hash_hex

# Пример использования
if __name__ == '__main__':
    print(generate_random_hash())
