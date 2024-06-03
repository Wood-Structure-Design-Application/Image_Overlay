import cv2
import sys
import os

# Get the directory where this script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Find the parent and grandparent directories
parent_directory = os.path.dirname(script_directory)
grandparent_directory = os.path.dirname(parent_directory)

# Print directories for verification (optional)
print(f"Script Directory: {script_directory}")
print(f"Parent Directory: {parent_directory}")
print(f"Grandparent Directory: {grandparent_directory}")

# Add the directories to sys.path
if script_directory not in sys.path:
    sys.path.append(script_directory)

if parent_directory not in sys.path:
    sys.path.append(parent_directory)

if grandparent_directory not in sys.path:
    sys.path.append(grandparent_directory)

# Print sys.path to verify (optional)
print("Updated sys.path:")
for path in sys.path:
    print(path)

# Import the modules
from Distance import PointDistanceCalculator
from FInd_point import ColorPointFinder
from Overlay import ResizeProcessor, TranslateProcessor, ImageOverlay



class CombineImage:
    def __init__(self, image_path1, image_path2):
        self.image_path1 = image_path1
        self.image_path2 = image_path2

    def point(self, color_range):

        color_point_finder = ColorPointFinder(self.image_path2)
        red_points, point2_image2 = color_point_finder.find_points()

        color_point_finder_blue = ColorPointFinder(self.image_path1)
        try:
            blue_points, point2_image1 = color_point_finder_blue.find_points("custom", color_range, color_range)
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

    def overlay(self, output_path, opacity_percent, color_range=None):

        overlay = ImageOverlay(self.image_path1, self.image_path2, output_path, opacity=opacity_percent)
        scale, point2_image1, point2_image2 = self.point(color_range)
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


if __name__ == "__main__":
    Opacity_percent = 40  # Example opacity percentage provided by the user
    Output_path = "overlay_image.png"
    Image1_path = "image1.png"
    Image2_path = "image2.png"
    comb = CombineImage(Image1_path, Image2_path)
    output = comb.overlay(Output_path, Opacity_percent)
    print(output)
