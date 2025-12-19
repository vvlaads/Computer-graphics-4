import numpy as np


def grid_centers(width_m, height_m, w_res, h_res):
    """Возвращает два массива координат центров пикселей по соответствующим осям"""
    step_x = width_m / w_res
    step_y = height_m / h_res

    x_centers = (-width_m / 2.0) + (np.arange(w_res) + 0.5) * step_x
    y_centers = (-height_m / 2.0) + (np.arange(h_res) + 0.5) * step_y
    return x_centers, y_centers
