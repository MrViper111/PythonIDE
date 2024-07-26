import cmu_graphics


class Colors:

    @staticmethod
    def parseRGB(values: list[int]) -> cmu_graphics.shape_logic.RGB:
        r = values[0]
        g = values[1]
        b = values[2]

        return cmu_graphics.shape_logic.RGB(r, g, b)
