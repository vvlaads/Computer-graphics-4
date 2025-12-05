def is_int(value):
    """Проверка, что значение является целым числом"""
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_float(value):
    """Проверка, что значение является вещественным числом"""
    try:
        float(value.replace(",", "."))
        return True
    except ValueError:
        return False
