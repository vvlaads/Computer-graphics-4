import math
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from layout_manager import LayoutManager
from validation import *
from illumination import *

# Глобальные переменные и константы
INT_MIN = -10 ** 9
img = None


def check_size_parameter(value):
    """Проверка параметра размера изображения"""
    result_value = INT_MIN
    error_message = ""

    if is_int(value):
        int_value = int(value)
        if int_value < 100 or int_value > 10000:
            error_message = "Введите число в диапазоне от 100 до 10000"
        else:
            result_value = int_value
    else:
        error_message = "Введите целое число"

    return result_value, error_message


def get_image_size():
    """Найти размер изображения"""
    # Проверяем значение H
    h_value = entry_h.get()
    h_value, h_error["text"] = check_size_parameter(h_value)

    # Проверяем значение W
    w_value = entry_w.get()
    w_value, w_error["text"] = check_size_parameter(w_value)

    return h_value, w_value


def check_resolution_parameter(value):
    """Проверка параметра разрешения изображения"""
    result_value = INT_MIN
    error_message = ""

    if is_int(value):
        int_value = int(value)
        if int_value < 200 or int_value > 800:
            error_message = "Введите число в диапазоне от 200 до 800"
        else:
            result_value = int_value
    else:
        error_message = "Введите целое число"

    return result_value, error_message


def get_image_resolution(height, width):
    """Найти разрешение изображения"""
    h_res_value = entry_h_res.get()
    h_res_value, h_res_error["text"] = check_resolution_parameter(h_res_value)

    w_res_value = entry_w_res.get()
    w_res_value, w_res_error["text"] = check_resolution_parameter(w_res_value)

    if h_res_value * width != w_res_value * height:
        h_res_value, w_res_value = -2, -2
    return h_res_value, w_res_value


def check_xy(value):
    """Проверка координаты X или Y"""
    result_value = INT_MIN
    error_message = ""

    if is_int(value):
        int_value = int(value)
        if int_value < -10000 or int_value > 10000:
            error_message = "Введите число в диапазоне от -10000 до 10000"
        else:
            result_value = int_value
    else:
        error_message = "Введите целое число"

    return result_value, error_message


def check_z(value):
    """Проверка координаты Z"""
    result_value = INT_MIN
    error_message = ""

    if is_int(value):
        int_value = int(value)
        if int_value < 100 or int_value > 10000:
            error_message = "Введите число в диапазоне от 100 до 10000"
        else:
            result_value = int_value
    else:
        error_message = "Введите целое число"

    return result_value, error_message


def get_coordinates():
    """Найти координаты источника света"""
    x_value = entry_x.get()
    x_value, x_error["text"] = check_xy(x_value)

    y_value = entry_y.get()
    y_value, y_error["text"] = check_xy(y_value)

    z_value = entry_z.get()
    z_value, z_error["text"] = check_z(z_value)
    return x_value, y_value, z_value


def check_power(value):
    """Проверка силы излучения"""
    result_value = INT_MIN
    error_message = ""

    if is_float(value):
        float_value = float(value.replace(",", "."))
        if float_value < 0.01 or float_value > 10000:
            error_message = "Введите число в диапазоне от 0.01 до 10000"
        else:
            result_value = float_value
    else:
        error_message = "Введите вещественное число"

    return result_value, error_message


def get_power():
    """Сила излучения"""
    power_value = entry_power.get()
    power_value, power_error["text"] = check_power(power_value)
    return power_value


def check_radius(value, height, width):
    """Проверка радиуса круга"""
    result_value = INT_MIN
    error_message = ""

    if is_int(value):
        int_value = int(value)
        if int_value < 1 or int_value > min(height, width) // 2:
            error_message = f"Введите число в диапазоне от 1 до {min(height, width) // 2}"
        else:
            result_value = int_value
    else:
        error_message = "Введите целое число"

    return result_value, error_message


def get_radius(height, width):
    """Радиус круга"""
    radius_value = entry_radius.get()
    radius_value, radius_error["text"] = check_radius(radius_value, height, width)
    return radius_value


def calculate():
    """Основной метод расчета"""
    global root, img, lm

    # Получение параметров
    h, w = get_image_size()
    if h == INT_MIN or w == INT_MIN:
        print("Ошибка размера изображения")
        return

    h_res, w_res = get_image_resolution(h, w)
    resolution_error["text"] = ""
    if h_res == INT_MIN or w_res == INT_MIN:
        print("Ошибка разрешения изображения")
        return
    elif h_res == -2 or w_res == -2:
        print("Разрешение не соответствует размерам")
        resolution_error["text"] = "Разрешение не соответствует размерам"
        return

    source_x, source_y, source_z = get_coordinates()
    if min(source_x, source_y, source_z) == INT_MIN:
        print("Ошибка координат источника света")
        return

    power = get_power()
    if power == INT_MIN:
        print("Ошибка силы излучения")
        return

    radius = get_radius(h, w)
    if radius == INT_MIN:
        print("Ошибка радиуса круга")
        return

    # Подсчёт освещенности
    x_centers, y_centers = grid_centers(w, h, w_res, h_res)
    light_list = [[0.0 for _ in range(w_res)] for _ in range(h_res)]

    for i in range(h_res):
        y = y_centers[i]
        for j in range(w_res):
            x = x_centers[j]
            light_list[i][j] = get_illumination(power, x, y, source_x, source_y, source_z)

    # Нормировка освещенности
    max_light = -1
    for i in range(h_res):
        max_light = max(max(light_list[i]), max_light)

    for i in range(h_res):
        for j in range(w_res):
            light_list[i][j] = int(255 * light_list[i][j] / max_light)

    # Создаем frame
    frame = ttk.Frame(root)
    frame.grid(row=0, column=3, rowspan=lm.get_row(), padx=20, pady=10)
    canvas = tk.Canvas(frame, height=700, width=800, name="image_canvas")

    # Полоса прокрутки
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Создаем изображение
    image = Image.new(mode="RGB", size=(w_res, h_res))
    for i in range(h_res):
        for j in range(w_res):
            color = light_list[i][j]
            image.putpixel((j, i), (color, color, color))

    img = image  # Сохраняем в глобальную переменную

    photo = ImageTk.PhotoImage(image)
    canvas.image = photo

    # Создаем изображение на canvas и устанавливаем область прокрутки
    canvas.create_image(0, 0, anchor='nw', image=photo)
    canvas.configure(scrollregion=canvas.bbox("all"))

    # Размещаем элементы
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Расчет освещенности в граничных точках круга
    print(f"Заданные параметры\n"
          f"W: {w}, H: {h}\n"
          f"W_res: {w_res}, H_res: {h_res}\n"
          f"(x, y, z): ({source_x}, {source_y}, {source_z})\n"
          f"I: {power}, радиус: {radius}\n"
          f"--- --- --- --- ---")

    for (x, y) in [(0, -radius), (0, radius), (-radius, 0), (radius, 0)]:
        illumination = get_illumination(power, x, y, source_x, source_y, source_z)
        print(f"E = {illumination: .4f} Вт/м^2 (x, y): ({x}, {y})")

    print("--- --- --- --- ---")

    # Построение графиков
    graph(w, h, w_res, h_res, source_x, source_y, source_z, power)


def save():
    """Сохранение полученного изображение в файл"""
    global img
    if img is None:
        print("Нечего сохранять")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"),
                                                        ("JPEG files", "*.jpg;*.jpeg"),
                                                        ("BMP files", "*.bmp")])
    if file_path:
        img.save(file_path)
        print(f"Изображение сохранено как {file_path}")


def graph(w, h, w_res, h_res, source_x, source_y, source_z, power):
    """Построение графиков сечения"""
    x_values, y_values = grid_centers(w, h, w_res, h_res)
    lights_x, lights_y = [], []

    # График по оси X
    for x in x_values:
        illumination = get_illumination(power, x, 0, source_x, source_y, source_z)
        lights_x.append(illumination)

    # График по оси Y
    for y in y_values:
        illumination = get_illumination(power, 0, y, source_x, source_y, source_z)
        lights_y.append(illumination)

    # Создаем фигуру с двумя подграфиками
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))  # 1 ряд, 2 колонки

    # Сечение вдоль X
    ax1.plot(x_values, lights_x, color='blue')
    ax1.set_xlabel('X, мм')
    ax1.set_ylabel('Освещенность E, Вт/м^2')
    ax1.set_title('Сечение вдоль X через центр области')
    ax1.grid(True)

    # Сечение вдоль Y
    ax2.plot(y_values, lights_y, color='red')
    ax2.set_xlabel('Y, мм')
    ax2.set_ylabel('Освещенность E, Вт/м^2')
    ax2.set_title('Сечение вдоль Y через центр области')
    ax2.grid(True)

    plt.tight_layout()
    plt.show()


# Создаем основное окно
root = tk.Tk()
root.title("Lab3")

# Получаем размеры экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Устанавливаем размер окна равным размеру экрана
root.geometry(f"{screen_width}x{screen_height}+0+0")
root.state('zoomed')

lm = LayoutManager()

# Подпись студента
student = tk.Label(root, text="Силинцев Владислав P3314")
student.grid(row=lm.get_row(), column=0, columnspan=2, pady=10)

# Разделитель перед следующим блоком
student_sep = ttk.Separator(root, orient=tk.HORIZONTAL)
student_sep.grid(row=lm.next_row(), column=0, columnspan=2, sticky="ew", pady=20)

# === Ввод размера области изображения ===
label_img_size = tk.Label(root, text="Размер области изображения (от 100 до 10000 мм)")
label_img_size.grid(row=lm.next_row(), column=0, padx=10, pady=5, columnspan=2)

label_h = tk.Label(root, text="Высота (H):")
label_h.grid(row=lm.next_row(), column=0, padx=10, pady=5)
entry_h = tk.Entry(root)
entry_h.grid(row=lm.get_row(), column=1, padx=10, pady=5)
h_error = tk.Label(root, text="")
h_error.grid(row=lm.get_row(), column=2, padx=10, pady=5)

label_w = tk.Label(root, text="Ширина (W):")
label_w.grid(row=lm.next_row(), column=0, padx=10, pady=5)
entry_w = tk.Entry(root)
entry_w.grid(row=lm.get_row(), column=1, padx=10, pady=5)
w_error = tk.Label(root, text="")
w_error.grid(row=lm.get_row(), column=2, padx=10, pady=5)

# Разделитель перед следующим блоком
img_size_sep = ttk.Separator(root, orient=tk.HORIZONTAL)
img_size_sep.grid(row=lm.next_row(), column=0, columnspan=2, sticky="ew", pady=20)

# === Ввод разрешения изображения ===
label_img_res = tk.Label(root, text="Разрешение изображения (от 200 до 800 пикселей)")
label_img_res.grid(row=lm.next_row(), column=0, padx=10, pady=5, columnspan=2)

label_h_res = tk.Label(root, text="Высота (Hres):")
label_h_res.grid(row=lm.next_row(), column=0, padx=10, pady=5)
entry_h_res = tk.Entry(root)
entry_h_res.grid(row=lm.get_row(), column=1, padx=10, pady=5)
h_res_error = tk.Label(root, text="")
h_res_error.grid(row=lm.get_row(), column=2, padx=10, pady=5)

label_w_res = tk.Label(root, text="Ширина (Wres):")
label_w_res.grid(row=lm.next_row(), column=0, padx=10, pady=5)
entry_w_res = tk.Entry(root)
entry_w_res.grid(row=lm.get_row(), column=1, padx=10, pady=5)
w_res_error = tk.Label(root, text="")
w_res_error.grid(row=lm.get_row(), column=2, padx=10, pady=5)

resolution_error = tk.Label(root, text="")
resolution_error.grid(row=lm.next_row(), column=0, padx=10, pady=5, columnspan=2)

# Разделитель перед следующим блоком
img_res_sep = ttk.Separator(root, orient=tk.HORIZONTAL)
img_res_sep.grid(row=lm.next_row(), column=0, columnspan=2, sticky="ew", pady=20)

# === Координаты источника света ===
label_img_res = tk.Label(root, text="Координаты источника света (мм)")
label_img_res.grid(row=lm.next_row(), column=0, padx=10, pady=5, columnspan=2)

label_x = tk.Label(root, text="X (от -10000 до 10000):")
label_x.grid(row=lm.next_row(), column=0, padx=10, pady=5)
entry_x = tk.Entry(root)
entry_x.grid(row=lm.get_row(), column=1, padx=10, pady=5)
x_error = tk.Label(root, text="")
x_error.grid(row=lm.get_row(), column=2, padx=10, pady=5)

label_y = tk.Label(root, text="Y (от -10000 до 10000):")
label_y.grid(row=lm.next_row(), column=0, padx=10, pady=5)
entry_y = tk.Entry(root)
entry_y.grid(row=lm.get_row(), column=1, padx=10, pady=5)
y_error = tk.Label(root, text="")
y_error.grid(row=lm.get_row(), column=2, padx=10, pady=5)

label_z = tk.Label(root, text="Z (от 100 до 10000):")
label_z.grid(row=lm.next_row(), column=0, padx=10, pady=5)
entry_z = tk.Entry(root)
entry_z.grid(row=lm.get_row(), column=1, padx=10, pady=5)
z_error = tk.Label(root, text="")
z_error.grid(row=lm.get_row(), column=2, padx=10, pady=5)

# Разделитель перед следующим блоком
coordinates_sep = ttk.Separator(root, orient=tk.HORIZONTAL)
coordinates_sep.grid(row=lm.next_row(), column=0, columnspan=2, sticky="ew", pady=20)

# === Сила излучения ===
label_power_head = tk.Label(root, text="Сила излучения (Вт/ср.)")
label_power_head.grid(row=lm.next_row(), column=0, padx=10, pady=5, columnspan=2)

label_power = tk.Label(root, text="I (от 0.01 до 10000):")
label_power.grid(row=lm.next_row(), column=0, padx=10, pady=5)
entry_power = tk.Entry(root)
entry_power.grid(row=lm.get_row(), column=1, padx=10, pady=5)
power_error = tk.Label(root, text="")
power_error.grid(row=lm.get_row(), column=2, padx=10, pady=5)

# Разделитель перед следующим блоком
power_sep = ttk.Separator(root, orient=tk.HORIZONTAL)
power_sep.grid(row=lm.next_row(), column=0, columnspan=2, sticky="ew", pady=20)

# === Радиус круга ===
label_radius_head = tk.Label(root, text="Радиус круга (мм)")
label_radius_head.grid(row=lm.next_row(), column=0, padx=10, pady=5, columnspan=2)

label_radius = tk.Label(root, text="R (от 1 до min(H, W) // 2):")
label_radius.grid(row=lm.next_row(), column=0, padx=10, pady=5)
entry_radius = tk.Entry(root)
entry_radius.grid(row=lm.get_row(), column=1, padx=10, pady=5)
radius_error = tk.Label(root, text="")
radius_error.grid(row=lm.get_row(), column=2, padx=10, pady=5)

# Разделитель перед следующим блоком
button_sep = ttk.Separator(root, orient=tk.HORIZONTAL)
button_sep.grid(row=lm.next_row(), column=0, columnspan=2, sticky="ew", pady=10)

# Кнопка для вычислений
button = tk.Button(root, text="Рассчитать", command=lambda: calculate(), width=15, height=2)
button.grid(row=lm.next_row(), column=0, padx=10, pady=5)

# Кнопка для сохранения
button = tk.Button(root, text="Сохранить", command=lambda: save(), width=15, height=2)
button.grid(row=lm.get_row(), column=1, padx=10, pady=5)

# Основной цикл
root.mainloop()
