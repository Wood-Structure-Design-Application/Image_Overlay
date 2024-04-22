class PointDistanceCalculator:
    @staticmethod
    def distance(points):
        x1, y1 = points[0]
        x2, y2 = points[1]
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
