import cv2
import numpy as np
from Distance import PointDistanceCalculator


class ColorPointFinder:
    def __init__(self, image_path):
        self.image_path = image_path

    def find_points(self, color_name="red", lower_range=None, upper_range=None):
        img = cv2.imread(self.image_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        if color_name.lower() == "blue":
            if lower_range is None:
                lower_range = np.array([0, 0, 100])
            if upper_range is None:
                upper_range = np.array([0, 255, 255])
        else:
            if lower_range is None:
                lower_range = np.array([100, 0, 0])
            if upper_range is None:
                upper_range = np.array([255, 100, 100])

        mask = cv2.inRange(img_rgb, lower_range, upper_range)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        points = []
        for contour in contours:
            M = cv2.moments(contour)
            if M["m00"] > 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                points.append((cx, cy))

        if len(points) >= 2:
            bluex = []
            for i in points:
                bluex.append(i[0])
            if bluex[0] > bluex[1]:
                point2_image = points[0]
            else:

                point2_image = points[1]
            return points[:2], point2_image
        else:
            print("Less than 2 points found.")
            return None, None


if __name__ == "__main__":
    image_path1 = "image1.png"
    image_path2 = "image2.png"

    color_point_finder = ColorPointFinder(image_path2)
    red_points, point2_image2 = color_point_finder.find_points()

    color_point_finder_blue = ColorPointFinder(image_path1)
    blue_points, point2_image1 = color_point_finder_blue.find_points(color_name="blue")
    #     [(196, 126), (569, 125)]
    # [(791, 3647), (3943, 3642)]
    if red_points and blue_points:
        dist_red = PointDistanceCalculator.distance(red_points)
        dist_blue = PointDistanceCalculator.distance(blue_points)
        print("Scale: ", dist_blue / dist_red)
        print("Red points coordinates:", red_points)
        print("Blue points coordinates:", blue_points)
        print("image1 point 2", point2_image1)
        print("image2 point 2", point2_image2)
        print("Length =", dist_red)
    else:
        print("Red points not found.")
