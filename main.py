import cv2
import numpy as np
from Distance import PointDistanceCalculator
from FInd_point import ColorPointFinder
from Overlay import ResizeProcessor, TranslateProcessor, ImageOverlay


class CombineImage:
    def __init__(self, image_path1, image_path2):
        self.image_path1 = image_path1
        self.image_path2 = image_path2

    def point(self):

        color_point_finder = ColorPointFinder(self.image_path2)
        red_points, point2_image2 = color_point_finder.find_points()

        color_point_finder_blue = ColorPointFinder(self.image_path1)
        try:
            blue_points, point2_image1 = color_point_finder_blue.find_points(color_name="blue")
        except cv2.error:
            print(cv2.error)
            return None, None, None
        if red_points and blue_points:
            dist_red = PointDistanceCalculator.distance(red_points)
            dist_blue = PointDistanceCalculator.distance(blue_points)
            scale = dist_blue / dist_red
            return scale, point2_image1, point2_image2

        else:
            print("Red points not found.")
            return None, None, None

    def overlay(self, output_path, opacity_percent):

        overlay = ImageOverlay(self.image_path1, self.image_path2, output_path, opacity=opacity_percent)
        scale, point2_image1, point2_image2 = self.point()
        if not scale:
            return False
        # Example points for demonstration, replace with your logic to find points
        point1_image2 = (0, 0)
        point1_image1 = (0, 0)

        resize_processor = ResizeProcessor(scale)
        translate_processor1 = TranslateProcessor(point1_image1[0] - point1_image2[0],
                                                  point1_image1[1] - point1_image2[1])
        translate_processor2 = TranslateProcessor(point2_image1[0] - point2_image2[0] * scale,
                                                  point2_image1[1] - point2_image2[1] * scale)

        overlay.combine_images_with_overlap(translate_processor1, translate_processor2, resize_processor)
        return True


Opacity_percent = 40  # Example opacity percentage provided by the user
Output_path = "overlay_image.png"
Image1_path = "image1.png"
Image2_path = "image2.png"
comb = CombineImage(Image1_path, Image2_path)
output = comb.overlay(Output_path, Opacity_percent)
print(output)
