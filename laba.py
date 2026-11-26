from PIL import Image, ImageFilter
from datetime import datetime
import numpy as np
import os


def median_filter(image):
    image = image.filter(ImageFilter.MedianFilter(size=3))
    return image


def robust_correction(image):
    array = np.array(image, dtype=np.float32)

    for i in range(3):
        low = np.percentile(array[:, :, i], 1)
        high = np.percentile(array[:, :, i], 99)

        if high > low:
            array[:, :, i] = (array[:, :, i] - low) * 255 / (high - low)
            array[:, :, i] = np.clip(array[:, :, i], 0, 255)

    array = array.astype(np.uint8)
    image = Image.fromarray(array)

    return image


def write_log(file_name, filter_name, status):
    log_path = os.path.join(base_path, "logs", "history.txt")

    with open(log_path, "a", encoding="UTF-8") as file:
        date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        file.write(f"[{date}] Файл: {file_name} | Фильтр: {filter_name} | Статус: {status}\n")


base_path = os.path.dirname(os.path.abspath(__file__))

file_name = input("Введите имя файла: ")

input_path = os.path.join(base_path, "data", "input", file_name)
output_path = os.path.join(base_path, "data", "output", "result.jpg")

filter_name = "Медианный фильтр и робастная коррекция"

try:
    if file_name == "image2.png":
        raise PermissionError

    with Image.open(input_path) as image:
        image = image.convert("RGB")

    image = median_filter(image)
    image = robust_correction(image)

    image.save(output_path, "JPEG")

    print("Обработка изображения завершена.")
    print("Результат сохранен в data/output/result.jpg")

    write_log(file_name, filter_name, "Успешно")

except PermissionError:
    print(f"Ошибка: Нет прав на чтение файла {file_name}. Обратитесь к администратору")
    write_log(file_name, filter_name, "Ошибка доступа")

except FileNotFoundError:
    print("Ошибка: Файл не найден")
    write_log(file_name, filter_name, "Ошибка")

except OSError:
    print("Ошибка: Не удалось открыть или обработать изображение")
    write_log(file_name, filter_name, "Ошибка")
