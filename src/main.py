import math
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from layout_manager import LayoutManager
from validation import *
from illumination import *
from util import *

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


def get_coordinates(number):
    """Найти координаты точки"""
    if number == 1:
        x_value = entry_x1.get()
        x_value, x1_error["text"] = check_xy(x_value)

        y_value = entry_y1.get()
        y_value, y1_error["text"] = check_xy(y_value)

        z_value = entry_z1.get()
        z_value, z1_error["text"] = check_z(z_value)
    elif number == 2:
        x_value = entry_x2.get()
        x_value, x2_error["text"] = check_xy(x_value)

        y_value = entry_y2.get()
        y_value, y2_error["text"] = check_xy(y_value)

        z_value = entry_z2.get()
        z_value, z2_error["text"] = check_z(z_value)
    else:
        x_value = entry_x_center.get()
        x_value, x_center_error["text"] = check_xy(x_value)

        y_value = entry_y_center.get()
        y_value, y_center_error["text"] = check_xy(y_value)

        z_value = entry_z_center.get()
        z_value, z_center_error["text"] = check_z(z_value)
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


def get_power(number):
    """Сила излучения"""
    if number == 1:
        power_value = entry_power1.get()
        power_value, power1_error["text"] = check_power(power_value)
    else:
        power_value = entry_power2.get()
        power_value, power2_error["text"] = check_power(power_value)
    return power_value


def check_radius(value):
    """Проверка радиуса сферы"""
    result_value = INT_MIN
    error_message = ""

    if is_float(value):
        float_value = float(value)
        if float_value < 0.01 or float_value > 10000:
            error_message = f"Введите число в диапазоне от 0.01 до 10000"
        else:
            result_value = float_value
    else:
        error_message = "Введите вещественное число"

    return result_value, error_message


def get_radius():
    """Радиус сферы"""
    radius_value = entry_radius.get()
    radius_value, radius_error["text"] = check_radius(radius_value)
    return radius_value


def check_observer(value):
    """Проверка координат наблюдателя"""
    result_value = INT_MIN
    error_message = ""

    if is_int(value):
        int_value = int(value)
        result_value = int_value
    else:
        error_message = "Введите целое число"

    return result_value, error_message


def get_observer():
    """Координаты наблюдателя"""
    z_value = entry_observer.get()
    z_value, observer_error["text"] = check_observer(z_value)
    return z_value


def check_kd(value):
    """Проверка диффузного отражения"""
    result_value = INT_MIN
    error_message = ""

    if is_float(value):
        float_value = float(value)
        if float_value < 0 or float_value > 1:
            error_message = "Введите значение из диапазона от 0 до 1"
        else:
            result_value = float_value
    else:
        error_message = "Введите вещественное число"

    return result_value, error_message


def get_kd():
    """Диффузное отражение"""
    value = entry_kd.get()
    value, kd_error["text"] = check_kd(value)
    return value


def check_ks(value):
    """Проверка зеркального отражения"""
    result_value = INT_MIN
    error_message = ""

    if is_float(value):
        float_value = float(value)
        if float_value < 0 or float_value > 1:
            error_message = "Введите значение из диапазона от 0 до 1"
        else:
            result_value = float_value
    else:
        error_message = "Введите вещественное число"

    return result_value, error_message


def get_ks():
    """Зеркальное отражение"""
    value = entry_ks.get()
    value, ks_error["text"] = check_ks(value)
    return value


def check_shininess(value):
    """Проверка блеска"""
    result_value = INT_MIN
    error_message = ""

    if is_int(value):
        int_value = int(value)
        if int_value < 0 or int_value > 10000:
            error_message = "Введите значение из диапазона от 0 до 10000"
        else:
            result_value = int_value
    else:
        error_message = "Введите целое число"

    return result_value, error_message


def get_shininess():
    """Блеск"""
    value = entry_shininess.get()
    value, shininess_error["text"] = check_shininess(value)
    return value


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

    source_x1, source_y1, source_z1 = get_coordinates(1)
    source_x2, source_y2, source_z2 = get_coordinates(2)
    if min(source_x1, source_y1, source_z1) == INT_MIN or min(source_x2, source_y2, source_z2) == INT_MIN:
        print("Ошибка координат источника света")
        return

    observer_z = get_observer()
    if observer_z == INT_MIN:
        print("Ошибка координат наблюдателя")
        return

    center_x, center_y, center_z = get_coordinates(3)
    if min(center_x, center_y, center_z) == INT_MIN:
        print("Ошибка координат центра сферы")
        return

    radius = get_radius()
    if radius == INT_MIN:
        print("Ошибка радиуса сферы")
        return

    power1 = get_power(1)
    power2 = get_power(2)
    if min(power1, power2) == INT_MIN:
        print("Ошибка силы излучения")
        return

    kd = get_kd()
    if kd == INT_MIN:
        print("Ошибка диффузного отражения")
        return

    ks = get_ks()
    if ks == INT_MIN:
        print("Ошибка зеркального отражения")
        return

    shininess = get_shininess()
    if shininess == INT_MIN:
        print("Ошибка блеска")
        return

    # === Подсчёт яркости ===
    brightness = [[0.0 for _ in range(w_res)] for _ in range(h_res)]

    # координаты наблюдателя и центра сферы
    observer = (0.0, 0.0, float(observer_z))
    sphere_center = (float(center_x), float(center_y), float(center_z))

    # источники
    light1 = (float(source_x1), float(source_y1), float(source_z1))
    light2 = (float(source_x2), float(source_y2), float(source_z2))

    x_centers, y_centers = grid_centers(w, h, w_res, h_res)
    for i in range(h_res):
        y = y_centers[i]
        for j in range(w_res):
            x = x_centers[j]
            # точка на плоскости z=0
            plane_point = (float(x), float(y), 0.0)
            obs_to_plane_point = vec_norm(vec_sub(plane_point, observer))

            intersection = intersection_with_sphere(observer, obs_to_plane_point, sphere_center, radius)
            brightness[i][j] = 0
            if intersection is not None:
                # Находим нормаль
                n = vec_norm(vec_sub(intersection, sphere_center))

                # Векторы к источникам света
                l1 = vec_norm(vec_sub(light1, intersection))
                l2 = vec_norm(vec_sub(light2, intersection))

                # Вектор к наблюдателю
                v = vec_norm(vec_sub(observer, intersection))

                # Вектор между источниками и наблюдателем
                h1 = vec_norm(vec_add(l1, v))
                h2 = vec_norm(vec_add(l2, v))

                # Диффузное и зеркальное отражение
                diff1 = kd * max(0, vec_dot(n, l1))
                spec1 = ks * max(0, vec_dot(n, h1)) ** shininess

                diff2 = kd * max(0, vec_dot(n, l2))
                spec2 = ks * max(0, vec_dot(n, h2)) ** shininess

                # Освещенность источником
                r1 = vec_len(vec_sub(light1, intersection))
                r2 = vec_len(vec_sub(light2, intersection))

                brightness[i][j] = (power1 / r1 ** 2) * (diff1 + spec1) + (power2 / r2 ** 2) * (diff2 + spec2)

    # Нормализация яркости
    max_brightness = max(max(row) for row in brightness)
    if max_brightness > 0:
        for i in range(h_res):
            for j in range(w_res):
                brightness[i][j] = int(255 * brightness[i][j] / max_brightness)

    # === Формирование изображения ===
    image = Image.new(mode="RGB", size=(w_res, h_res))
    for i in range(h_res):
        for j in range(w_res):
            c = brightness[i][j]
            image.putpixel((j, i), (c, c, c))

    img = image  # Сохраняем в глобальную переменную

    # Показать в canvas
    frame = ttk.Frame(root)
    frame.grid(row=0, column=6, rowspan=lm.get_row(), padx=20, pady=10)
    canvas = tk.Canvas(frame, height=800, width=800, name="image_canvas")
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    photo = ImageTk.PhotoImage(image)
    canvas.image = photo
    canvas.create_image(0, 0, anchor='nw', image=photo)
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")


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
label_coordinates1 = tk.Label(root, text="Координаты 1 источника света (мм)")
label_coordinates1.grid(row=lm.next_row(), column=0, padx=10, pady=5, columnspan=2)

label_x1 = tk.Label(root, text="X (от -10000 до 10000):")
label_x1.grid(row=lm.next_row(), column=0, padx=10, pady=5)
entry_x1 = tk.Entry(root)
entry_x1.grid(row=lm.get_row(), column=1, padx=10, pady=5)
x1_error = tk.Label(root, text="")
x1_error.grid(row=lm.get_row(), column=2, padx=10, pady=5)

label_y1 = tk.Label(root, text="Y (от -10000 до 10000):")
label_y1.grid(row=lm.next_row(), column=0, padx=10, pady=5)
entry_y1 = tk.Entry(root)
entry_y1.grid(row=lm.get_row(), column=1, padx=10, pady=5)
y1_error = tk.Label(root, text="")
y1_error.grid(row=lm.get_row(), column=2, padx=10, pady=5)

label_z1 = tk.Label(root, text="Z (от 100 до 10000):")
label_z1.grid(row=lm.next_row(), column=0, padx=10, pady=5)
entry_z1 = tk.Entry(root)
entry_z1.grid(row=lm.get_row(), column=1, padx=10, pady=5)
z1_error = tk.Label(root, text="")
z1_error.grid(row=lm.get_row(), column=2, padx=10, pady=5)

# Разделитель перед следующим блоком
coordinates1_sep = ttk.Separator(root, orient=tk.HORIZONTAL)
coordinates1_sep.grid(row=lm.next_row(), column=0, columnspan=2, sticky="ew", pady=20)

label_coordinates2 = tk.Label(root, text="Координаты 2 источника света (мм)")
label_coordinates2.grid(row=lm.next_row(), column=0, padx=10, pady=5, columnspan=2)

label_x2 = tk.Label(root, text="X (от -10000 до 10000):")
label_x2.grid(row=lm.next_row(), column=0, padx=10, pady=5)
entry_x2 = tk.Entry(root)
entry_x2.grid(row=lm.get_row(), column=1, padx=10, pady=5)
x2_error = tk.Label(root, text="")
x2_error.grid(row=lm.get_row(), column=2, padx=10, pady=5)

label_y2 = tk.Label(root, text="Y (от -10000 до 10000):")
label_y2.grid(row=lm.next_row(), column=0, padx=10, pady=5)
entry_y2 = tk.Entry(root)
entry_y2.grid(row=lm.get_row(), column=1, padx=10, pady=5)
y2_error = tk.Label(root, text="")
y2_error.grid(row=lm.get_row(), column=2, padx=10, pady=5)

label_z2 = tk.Label(root, text="Z (от 100 до 10000):")
label_z2.grid(row=lm.next_row(), column=0, padx=10, pady=5)
entry_z2 = tk.Entry(root)
entry_z2.grid(row=lm.get_row(), column=1, padx=10, pady=5)
z2_error = tk.Label(root, text="")
z2_error.grid(row=lm.get_row(), column=2, padx=10, pady=5)

# Разделитель перед следующим блоком
coordinates_sep = ttk.Separator(root, orient=tk.HORIZONTAL)
coordinates_sep.grid(row=lm.next_row(), column=0, columnspan=2, sticky="ew", pady=20)

lm.clear()

# Разделитель перед следующим блоком
new_sep = ttk.Separator(root, orient=tk.HORIZONTAL)
new_sep.grid(row=lm.next_row(), column=3, columnspan=2, sticky="ew", pady=20)

# === Координаты наблюдателя ===
observer_head = tk.Label(root, text="Координаты наблюдателя")
observer_head.grid(row=lm.next_row(), column=3, padx=10, pady=5, columnspan=2)

label_observer = tk.Label(root, text="z:")
label_observer.grid(row=lm.next_row(), column=3, padx=10, pady=5)
entry_observer = tk.Entry(root)
entry_observer.grid(row=lm.get_row(), column=4, padx=10, pady=5)
observer_error = tk.Label(root, text="")
observer_error.grid(row=lm.get_row(), column=5, padx=10, pady=5)

# Разделитель перед следующим блоком
observer_sep = ttk.Separator(root, orient=tk.HORIZONTAL)
observer_sep.grid(row=lm.next_row(), column=3, columnspan=2, sticky="ew", pady=20)

# === Координаты центра сферы ===
label_center = tk.Label(root, text="Координаты центра сферы (мм)")
label_center.grid(row=lm.next_row(), column=3, padx=10, pady=5, columnspan=2)

label_x_center = tk.Label(root, text="X (от -10000 до 10000):")
label_x_center.grid(row=lm.next_row(), column=3, padx=10, pady=5)
entry_x_center = tk.Entry(root)
entry_x_center.grid(row=lm.get_row(), column=4, padx=10, pady=5)
x_center_error = tk.Label(root, text="")
x_center_error.grid(row=lm.get_row(), column=5, padx=10, pady=5)

label_y_center = tk.Label(root, text="Y (от -10000 до 10000):")
label_y_center.grid(row=lm.next_row(), column=3, padx=10, pady=5)
entry_y_center = tk.Entry(root)
entry_y_center.grid(row=lm.get_row(), column=4, padx=10, pady=5)
y_center_error = tk.Label(root, text="")
y_center_error.grid(row=lm.get_row(), column=5, padx=10, pady=5)

label_z_center = tk.Label(root, text="Z (от 100 до 10000):")
label_z_center.grid(row=lm.next_row(), column=3, padx=10, pady=5)
entry_z_center = tk.Entry(root)
entry_z_center.grid(row=lm.get_row(), column=4, padx=10, pady=5)
z_center_error = tk.Label(root, text="")
z_center_error.grid(row=lm.get_row(), column=5, padx=10, pady=5)

# Разделитель перед следующим блоком
coordinates_center_sep = ttk.Separator(root, orient=tk.HORIZONTAL)
coordinates_center_sep.grid(row=lm.next_row(), column=3, columnspan=2, sticky="ew", pady=20)

# === Координаты центра сферы ===
label_radius_head = tk.Label(root, text="Радиус сферы (мм)")
label_radius_head.grid(row=lm.next_row(), column=3, padx=10, pady=5, columnspan=2)

label_radius = tk.Label(root, text="R (от 0.01 до 10000):")
label_radius.grid(row=lm.next_row(), column=3, padx=10, pady=5)
entry_radius = tk.Entry(root)
entry_radius.grid(row=lm.get_row(), column=4, padx=10, pady=5)
radius_error = tk.Label(root, text="")
radius_error.grid(row=lm.get_row(), column=5, padx=10, pady=5)

# Разделитель перед следующим блоком
radius_sep = ttk.Separator(root, orient=tk.HORIZONTAL)
radius_sep.grid(row=lm.next_row(), column=3, columnspan=2, sticky="ew", pady=20)

# === Сила излучения ===
label_power_head = tk.Label(root, text="Сила излучения (Вт/ср.)")
label_power_head.grid(row=lm.next_row(), column=3, padx=10, pady=5, columnspan=2)

label_power1 = tk.Label(root, text="I1 (от 0.01 до 10000):")
label_power1.grid(row=lm.next_row(), column=3, padx=10, pady=5)
entry_power1 = tk.Entry(root)
entry_power1.grid(row=lm.get_row(), column=4, padx=10, pady=5)
power1_error = tk.Label(root, text="")
power1_error.grid(row=lm.get_row(), column=5, padx=10, pady=5)

label_power2 = tk.Label(root, text="I2 (от 0.01 до 10000):")
label_power2.grid(row=lm.next_row(), column=3, padx=10, pady=5)
entry_power2 = tk.Entry(root)
entry_power2.grid(row=lm.get_row(), column=4, padx=10, pady=5)
power2_error = tk.Label(root, text="")
power2_error.grid(row=lm.get_row(), column=5, padx=10, pady=5)

# Разделитель перед следующим блоком
power_sep = ttk.Separator(root, orient=tk.HORIZONTAL)
power_sep.grid(row=lm.next_row(), column=3, columnspan=2, sticky="ew", pady=20)

# === Диффузное отражение ===
label_kd_head = tk.Label(root, text="Диффузное отражение")
label_kd_head.grid(row=lm.next_row(), column=3, padx=10, pady=5, columnspan=2)

label_kd = tk.Label(root, text="k_d (от 0 до 1):")
label_kd.grid(row=lm.next_row(), column=3, padx=10, pady=5)
entry_kd = tk.Entry(root)
entry_kd.grid(row=lm.get_row(), column=4, padx=10, pady=5)
kd_error = tk.Label(root, text="")
kd_error.grid(row=lm.get_row(), column=5, padx=10, pady=5)

# Разделитель перед следующим блоком
kd_sep = ttk.Separator(root, orient=tk.HORIZONTAL)
kd_sep.grid(row=lm.next_row(), column=3, columnspan=2, sticky="ew", pady=10)

# === Зеркальное отражение ===
label_ks_head = tk.Label(root, text="Зеркальное отражение")
label_ks_head.grid(row=lm.next_row(), column=3, padx=10, pady=5, columnspan=2)

label_ks = tk.Label(root, text="k_s (от 0 до 1):")
label_ks.grid(row=lm.next_row(), column=3, padx=10, pady=5)
entry_ks = tk.Entry(root)
entry_ks.grid(row=lm.get_row(), column=4, padx=10, pady=5)
ks_error = tk.Label(root, text="")
ks_error.grid(row=lm.get_row(), column=5, padx=10, pady=5)

# Разделитель перед следующим блоком
kd_sep = ttk.Separator(root, orient=tk.HORIZONTAL)
kd_sep.grid(row=lm.next_row(), column=3, columnspan=2, sticky="ew", pady=10)

# === Блеск ===
label_shininess_head = tk.Label(root, text="Блеск")
label_shininess_head.grid(row=lm.next_row(), column=3, padx=10, pady=5, columnspan=2)

label_shininess = tk.Label(root, text="shininess (от 0 до 10000):")
label_shininess.grid(row=lm.next_row(), column=3, padx=10, pady=5)
entry_shininess = tk.Entry(root)
entry_shininess.grid(row=lm.get_row(), column=4, padx=10, pady=5)
shininess_error = tk.Label(root, text="")
shininess_error.grid(row=lm.get_row(), column=5, padx=10, pady=5)

# Разделитель перед следующим блоком
button_sep = ttk.Separator(root, orient=tk.HORIZONTAL)
button_sep.grid(row=lm.next_row(), column=3, columnspan=2, sticky="ew", pady=10)

# Кнопка для вычислений
button = tk.Button(root, text="Рассчитать", command=lambda: calculate(), width=15, height=2)
button.grid(row=lm.next_row(), column=3, padx=10, pady=5)

# Кнопка для сохранения
button = tk.Button(root, text="Сохранить", command=lambda: save(), width=15, height=2)
button.grid(row=lm.get_row(), column=4, padx=10, pady=5)

# Основной цикл
root.mainloop()
