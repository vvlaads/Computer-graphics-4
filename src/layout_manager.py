class LayoutManager:
    """Вспомогательный класс для расположения элементов интерфейса в табличной форме"""

    def __init__(self):
        self.row_number = 0

    def next_row(self):
        self.row_number += 1
        return self.row_number

    def get_row(self):
        return self.row_number

    def clear(self):
        self.row_number = 0
