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
MM_TO_M = 0.001
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


def check_intensity(value):
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


def get_intensity(number):
    """Интенсивность излучения"""
    if number == 1:
        intensity_value = entry_intensity1.get()
        intensity_value, intensity1_error["text"] = check_intensity(intensity_value)
    else:
        intensity_value = entry_intensity2.get()
        intensity_value, intensity2_error["text"] = check_intensity(intensity_value)
    return intensity_value


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


def check_sphere_visibility(observer, sphere_center, radius_m, w_m, h_m):
    """Проверяет, что сфера целиком помещается в область видимости наблюдателя"""

    # Проверяем, что наблюдатель не внутри сферы
    observer_to_center = vec_sub(observer, sphere_center)
    distance_to_center = vec_len(observer_to_center)

    if distance_to_center <= radius_m:
        return False, "Наблюдатель находится внутри или на поверхности сферы"

    # Проверяем, что сфера полностью перед наблюдателем
    if sphere_center[2] + radius_m >= observer[2]:
        return False, "Сфера находится выше наблюдателя"

    obs_x, obs_y, obs_z = observer

    # Проектируем сферу на плоскость z=0 (плоскость изображения)
    # Используем подобие треугольников
    t = -obs_z / (sphere_center[2] - obs_z)

    # Проекция центра сферы
    proj_center_x = obs_x + t * (sphere_center[0] - obs_x)
    proj_center_y = obs_y + t * (sphere_center[1] - obs_y)

    # Радиус проекции (подобие треугольников)
    proj_radius = radius_m * abs(t) / distance_to_center

    # Границы области видимости на плоскости z=0
    left = -w_m / 2
    right = w_m / 2
    bottom = -h_m / 2
    top = h_m / 2

    # Проверяем, что проекция сферы полностью внутри прямоугольника
    if (proj_center_x - proj_radius < left or
            proj_center_x + proj_radius > right or
            proj_center_y - proj_radius < bottom or
            proj_center_y + proj_radius > top):
        return False, "Проекция сферы выходит за границы видимой области"

    # Также проверяем, что сфера не слишком близко к границам
    margin = min(w_m, h_m) * 0.05  # 5% отступ

    if (proj_center_x - proj_radius < left + margin or
            proj_center_x + proj_radius > right - margin or
            proj_center_y - proj_radius < bottom + margin or
            proj_center_y + proj_radius > top - margin):
        return False, "Сфера слишком близко к границе видимой области"

    return True, ""


def check_lights(observer, light1, light2, sphere_center, radius_m):
    """
    Проверяет, что источники света не находятся внутри сферы или за ней.
    """
    # Вектор от наблюдателя к источнику света 1
    dir_to_light1 = vec_norm(vec_sub(light1, observer))

    # Проверяем пересечение этого луча со сферой
    intersection1 = intersection_with_sphere(observer, dir_to_light1, sphere_center, radius_m)
    if intersection1 is not None:
        # Проверяем, находится ли источник за сферой
        dist_to_intersection = vec_len(vec_sub(intersection1, observer))
        dist_to_light = vec_len(vec_sub(light1, observer))
        if dist_to_intersection < dist_to_light - 1e-6:
            return False, "Источник света 1 находится в тени сферы"

    # Аналогично для второго источника
    dir_to_light2 = vec_norm(vec_sub(light2, observer))
    intersection2 = intersection_with_sphere(observer, dir_to_light2, sphere_center, radius_m)
    if intersection2 is not None:
        dist_to_intersection = vec_len(vec_sub(intersection2, observer))
        dist_to_light = vec_len(vec_sub(light2, observer))
        if dist_to_intersection < dist_to_light - 1e-6:
            return False, "Источник света 2 находится в тени сферы"

    # Проверяем, что источники не внутри сферы
    dist1 = vec_len(vec_sub(light1, sphere_center))
    if dist1 <= radius_m:
        return False, "Источник света 1 находится внутри сферы"

    dist2 = vec_len(vec_sub(light2, sphere_center))
    if dist2 <= radius_m:
        return False, "Источник света 2 находится внутри сферы"

    return True, ""


def calculate():
    """Основной метод расчета"""
    global root, img, lm

    # === Получение параметров ===
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

    intensity1 = get_intensity(1)
    intensity2 = get_intensity(2)
    if min(intensity1, intensity2) == INT_MIN:
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

    # === Подготовка данных ===
    # координаты наблюдателя и центра сферы
    observer = (0.0, 0.0, float(observer_z) * MM_TO_M)
    sphere_center = (float(center_x) * MM_TO_M, float(center_y) * MM_TO_M, float(center_z) * MM_TO_M)

    # источники
    light1 = (float(source_x1) * MM_TO_M, float(source_y1) * MM_TO_M, float(source_z1) * MM_TO_M)
    light2 = (float(source_x2) * MM_TO_M, float(source_y2) * MM_TO_M, float(source_z2) * MM_TO_M)

    # радиус в м
    radius_m = radius * MM_TO_M

    # размеры области в м
    w_m = w * MM_TO_M
    h_m = h * MM_TO_M

    # Очищаем сообщения об ошибке
    sphere_visible_error["text"] = ""
    lights_error["text"] = ""

    is_sphere_visible, sphere_visible_error["text"] = check_sphere_visibility(observer, sphere_center, radius_m, w_m,
                                                                              h_m)
    if not is_sphere_visible:
        print("Ошибка! Сфера не помещается целиком в область видимости")
        return

    are_lights_ok, lights_error["text"] = check_lights(observer, light1, light2, sphere_center, radius_m)
    if not are_lights_ok:
        print("Источник света находится внутри сферы")
        return

    # === Подсчёт яркости ===
    brightness = [[0.0 for _ in range(w_res)] for _ in range(h_res)]
    x_centers, y_centers = grid_centers(w_m, h_m, w_res, h_res)
    for i in range(h_res):
        y = y_centers[i]
        for j in range(w_res):
            x = x_centers[j]
            # точка на плоскости z=0
            plane_point = (float(x), float(y), 0.0)
            obs_to_plane_point = vec_norm(vec_sub(plane_point, observer))

            intersection = intersection_with_sphere(observer, obs_to_plane_point, sphere_center, radius_m)
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

                brightness[i][j] = intensity1 * (diff1 + spec1) + intensity2 * (diff2 + spec2)

    # Значения яркости в некоторых точках на сфере
    min_brightness = min(min(row) for row in brightness)
    max_brightness = max(max(row) for row in brightness)
    point_brightness = get_brightness_in_points(observer,
                                                light1, light2,
                                                sphere_center, radius_m,
                                                kd, ks, shininess, intensity1, intensity2)

    print("=" * 100)
    print(f"Минимальное значение яркости: {min_brightness}")
    print(f"Максимальное значение яркости: {max_brightness}")
    for (point, brightness_val) in point_brightness:
        print(f"Точка ({point[0]: .3f}, {point[1]: .3f}, {point[2]: .3f}) (м): яркость = {brightness_val: .6f}")
    print("=" * 100)

    # Нормализация яркости
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


def get_brightness_in_points(observer, light1, light2, sphere_center, radius_m, kd, ks, shininess, intensity1,
                             intensity2):
    """Расчет яркости в 3 точках сферы"""

    # Выбираем 3 характерные точки на сфере:
    # 1) Точка, направленная к первому источнику
    # 2) Точка, направленная ко второму источнику
    # 3) Произвольная точка

    # Список для хранения яркости в 3 точках
    point_brightness = []

    # Вычисляем векторы от центра сферы к источникам
    light1_dir = vec_norm(vec_sub(light1, sphere_center))
    light2_dir = vec_norm(vec_sub(light2, sphere_center))

    # Точки на поверхности сферы:
    # Точка 1: в направлении первого источника
    point1 = (
        sphere_center[0] + light1_dir[0] * radius_m,
        sphere_center[1] + light1_dir[1] * radius_m,
        sphere_center[2] + light1_dir[2] * radius_m
    )

    # Точка 2: в направлении второго источника
    point2 = (
        sphere_center[0] + light2_dir[0] * radius_m,
        sphere_center[1] + light2_dir[1] * radius_m,
        sphere_center[2] + light2_dir[2] * radius_m
    )

    # Точка 3: произвольная точка
    arbitrary_dir = (0.0, 1.0, 0.0)  # например, по оси Y
    point3 = (
        sphere_center[0] + arbitrary_dir[0] * radius_m,
        sphere_center[1] + arbitrary_dir[1] * radius_m,
        sphere_center[2] + arbitrary_dir[2] * radius_m
    )

    # Вычисляем яркость в этих точках
    selected_points = [point1, point2, point3]

    for idx, point in enumerate(selected_points, 1):
        # Нормаль в этой точке (от центра к поверхности)
        n = vec_norm(vec_sub(point, sphere_center))

        # Векторы к источникам света
        l1 = vec_norm(vec_sub(light1, point))
        l2 = vec_norm(vec_sub(light2, point))

        # Вектор к наблюдателю
        v = vec_norm(vec_sub(observer, point))

        # Half-vectors
        h1 = vec_norm(vec_add(l1, v))
        h2 = vec_norm(vec_add(l2, v))

        # Диффузное и зеркальное отражение
        diff1 = kd * max(0, vec_dot(n, l1))
        spec1 = ks * max(0, vec_dot(n, h1)) ** shininess

        diff2 = kd * max(0, vec_dot(n, l2))
        spec2 = ks * max(0, vec_dot(n, h2)) ** shininess

        # Яркость в этой точке
        point_brightness_val = intensity1 * (diff1 + spec1) + intensity2 * (diff2 + spec2)
        point_brightness.append((point, point_brightness_val))

    return point_brightness


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

# === Интенсивность излучения ===
label_intensity_head = tk.Label(root, text="Интенсивность излучения (Вт/ср.)")
label_intensity_head.grid(row=lm.next_row(), column=3, padx=10, pady=5, columnspan=2)

label_intensity1 = tk.Label(root, text="I1 (от 0.01 до 10000):")
label_intensity1.grid(row=lm.next_row(), column=3, padx=10, pady=5)
entry_intensity1 = tk.Entry(root)
entry_intensity1.grid(row=lm.get_row(), column=4, padx=10, pady=5)
intensity1_error = tk.Label(root, text="")
intensity1_error.grid(row=lm.get_row(), column=5, padx=10, pady=5)

label_intensity2 = tk.Label(root, text="I2 (от 0.01 до 10000):")
label_intensity2.grid(row=lm.next_row(), column=3, padx=10, pady=5)
entry_intensity2 = tk.Entry(root)
entry_intensity2.grid(row=lm.get_row(), column=4, padx=10, pady=5)
intensity2_error = tk.Label(root, text="")
intensity2_error.grid(row=lm.get_row(), column=5, padx=10, pady=5)

# Разделитель перед следующим блоком
intensity_sep = ttk.Separator(root, orient=tk.HORIZONTAL)
intensity_sep.grid(row=lm.next_row(), column=3, columnspan=2, sticky="ew", pady=20)

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

sphere_visible_error = tk.Label(root, text="")
sphere_visible_error.grid(row=lm.next_row(), column=3, padx=10, pady=5, columnspan=2)

lights_error = tk.Label(root, text="")
lights_error.grid(row=lm.next_row(), column=3, padx=10, pady=5, columnspan=2)

# Основной цикл
root.mainloop()
