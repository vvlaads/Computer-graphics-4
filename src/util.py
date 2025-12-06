import math


def vec_sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def vec_add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def vec_scale(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)


def vec_dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vec_len(a):
    return math.sqrt(vec_dot(a, a))


def vec_norm(a):
    length = vec_len(a)
    if length < 1e-12: return (0.0, 0.0, 0.0)
    return (a[0] / length, a[1] / length, a[2] / length)


def intersection_with_sphere(obs, vec, center, radius):
    obs_to_center = vec_sub(obs, center)
    A = vec_dot(vec, vec)  # обычно 1
    B = 2.0 * vec_dot(vec, obs_to_center)
    C = vec_dot(obs_to_center, obs_to_center) - radius * radius
    D = B * B - 4 * A * C
    if D < 0:
        return None  # нет пересечения
    sqrtD = D ** 0.5
    t1 = (-B - sqrtD) / (2 * A)
    t2 = (-B + sqrtD) / (2 * A)
    # выбрать ближайшую положительную t
    ts = [t for t in (t1, t2) if t > 1e-6]
    if not ts:
        return None
    t = min(ts)
    # возвращаем параметр t и саму точку пересечения
    point = vec_add(obs, vec_scale(vec, t))
    return point
