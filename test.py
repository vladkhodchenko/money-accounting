class Entity:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y


class SquareMixin:
    def __init__(self, size, **kwargs):
        # super().__init__(**kwargs)
        self.size_x = size
        self.size_y = size

    def perimeter(self):
        return self.size_x * 4

    def square(self):
        return self.size_x * self.size_x


class SquareEntity(SquareMixin, Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)