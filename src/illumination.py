import numpy as np


def get_illumination(power, px_mm, py_mm, sx_mm, sy_mm, sz_mm):
    """Формула подсчета освещенности в точке на плоскости z = 0 от точечного источника света"""
    diff_x = abs(px_mm - sx_mm) / 1000
    diff_y = abs(py_mm - sy_mm) / 1000
    diff_z = sz_mm / 1000

    distance = diff_x ** 2 + diff_y ** 2 + diff_z ** 2
    cos = diff_z / distance

    return power * cos / (distance ** 2)


def grid_centers(width_mm, height_mm, w_res, h_res):
    """Возвращает два массива координат центров пикселей по соответствующим осям"""
    step_x = width_mm / w_res
    step_y = height_mm / h_res

    x_centers = (-width_mm / 2.0) + (np.arange(w_res) + 0.5) * step_x
    y_centers = (-height_mm / 2.0) + (np.arange(h_res) + 0.5) * step_y
    return x_centers, y_centers
