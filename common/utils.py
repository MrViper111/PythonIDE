import math


class Utils:

    @staticmethod
    def distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    def build_string(*lines):
        return "\n".join(lines)
