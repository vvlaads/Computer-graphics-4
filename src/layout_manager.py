class LayoutManager:
    """Вспомогательный класс для расположения элементов интерфейса в табличной форме"""

    def __init__(self):
        """Конструктор"""
        self.row_number = 0

    def next_row(self):
        """Вернуть номер следующей строки"""
        self.row_number += 1
        return self.row_number

    def get_row(self):
        """Вернуть номер текущей строки"""
        return self.row_number

    def clear(self):
        """Обнулить номер строки"""
        self.row_number = 0
