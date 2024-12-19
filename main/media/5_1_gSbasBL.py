import numpy as np

k = int(input("Введите количество информационных разрядов: "))

r = 0
while (2 ** r) < (k + r + 1):
    r += 1

rows = r
cols = k + r + 1
table = np.zeros((rows, cols), dtype=int)

# Заполняем таблицу двоичными представлениями чисел
for col in range(1, cols):
    binary = format(col, f'0{rows}b')
    for row in range(rows):
        table[row][col] = int(binary[row])

# Генерируем случайную последовательность

data = ''.join([str(np.random.randint(0, 2)) for _ in range(k)])
print(f"Исходные данные: {data}")

print(f"Проверочная таблица: \n{table}")


# Находим позиции проверочных битов
check_positions = []
i = 1
while i <= (k + r):
    check_positions.append(i)
    i *= 2
print(f"Проверочные биты в позиции: {check_positions}")

# Создаем закодированное сообщение
encoded = np.zeros(len(data) + len(check_positions), dtype=int)

# Размещаем информационные биты
data_idx = 0
j = 0
for i in range(1, len(encoded) + 1):
    if j < len(check_positions) and i == check_positions[j]:
        j += 1
    else:
        encoded[i - 1] = int(data[data_idx])
        data_idx += 1

# Вычисляем проверочные биты
for pos in check_positions:
    check_sum = 0
    for i in range(1, len(encoded) + 1):
        if i != pos and (i & pos) != 0:
            check_sum ^= encoded[i - 1]
    encoded[pos - 1] = check_sum

print(f"Закодированные данные: {''.join(map(str, encoded))}")

# Создание ошибки
error_position = np.random.randint(0, len(encoded))
encoded[error_position] ^= 1  # Изменяем бит
print(f"Данные с ошибкой: {''.join(map(str, encoded))}")

# Поиск ошибки по синдрому
syndrome = np.zeros(rows, dtype=int)

for row in range(rows):
    check_sum = 0
    for col in range(1, table.shape[1]):
        check_sum ^= (encoded[col - 1] * table[row][col])
    syndrome[row] = check_sum

syndrome = syndrome[::-1]
print(f"Синдром: {syndrome}")

error_position = 0
for i in range(len(syndrome)):
    error_position += syndrome[i] * (2 ** i)

print(f"Ошибка обнаружена в позиции: {error_position}")

encoded[error_position - 1] ^= 1
print(f"Исправленные данные: {''.join(map(str, encoded))}")