# Line Class, made specifically for trilateration
# Most functions would be useless in other cases
from itertools import combinations
class Line:
    def __init__(self, x, i, vertical=False):
        self.x = x
        self.i = i
        self.vertical = vertical
        # If Vertical, i becomes the "shift", like in the equation: x = i

    def draw(self, canvas):
        if self.vertical:
            canvas.create_line(self.i, 0, self.i, 1000, fill="green")
        else:
            canvas.create_line(0, self.i, 1000, self.x * 1000 + self.i, fill="green")

    # Takes two lines and finds where they intersect
    # After getting two lines from get_line, this finds where they intersect and therefore where the circles intersect
    def get_intersect(self, other_line1, other_line2):
        # 3 lines given, finds the intersect of two that don't error
        for t in combinations([self, other_line1, other_line2], 2):
            if t[0].vertical and t[1].vertical: # Parallel Lines
                continue
            if t[0].vertical:
                return t[0].i, t[1].x*t[0].i+t[1].i
            if t[1].vertical:
                return t[1].i, t[0].x*t[1].i+t[0].i
            x1, i1 = t[0].x, t[0].i
            x2, i2 = t[1].x, t[1].i
            x = x1 - x2
            i = i2 - i1
            try:
                x = i / x
            except ZeroDivisionError:  # Parallel Lines
                continue
            else:
                y = x1 * x + i1
                return x, y
        raise Exception("All Lines are Parallel")

