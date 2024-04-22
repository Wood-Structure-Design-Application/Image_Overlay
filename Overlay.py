import cv2
import numpy as np


class ImageProcessor:
    def process(self, image):
        raise NotImplementedError


class ResizeProcessor(ImageProcessor):
    def __init__(self, scale):
        self.scale = scale

    def process(self, image):
        return cv2.resize(image, None, fx=self.scale, fy=self.scale, interpolation=cv2.INTER_LINEAR)


# The `TranslateProcessor` class implements an image processing technique to translate an image by a specified
# displacement in the x and y directions.
class TranslateProcessor(ImageProcessor):
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def process(self, image, image_shape=np.array([0])):
        """
        The function takes an image and applies a 2D translation transformation to it using OpenCV.

        :param image_shape:
        :param image: The `image` parameter in the `process` function is expected to be a NumPy array representing an image.
        The function processes this image by applying an affine transformation using OpenCV's `cv2.warpAffine` function. The
        transformation is defined by a 2x3 transformation matrix `
        :return: the input image after applying an affine transformation to it. The transformation is defined by the matrix
        `M`, which includes translation parameters `self.dx` and `self.dy`. The `cv2.warpAffine` function is used to perform
        the transformation on the input image.
        """
        if image_shape.any():
            rows, cols, _ = image_shape.shape
        else:
            rows, cols, _ = image.shape
        M = np.float32([[1, 0, self.dx], [0, 1, self.dy]])
        return cv2.warpAffine(image, M, (cols, rows))


class ImageOverlay:
    def __init__(self, image1_path, image2_path, output_path, opacity=50):
        self.image1_path = image1_path
        self.image2_path = image2_path
        self.output_path = output_path
        self.opacity = opacity

    def combine_images_with_overlap(self, processor1, processor2, resizer):
        image1 = cv2.imread(self.image1_path)
        image2 = cv2.imread(self.image2_path)

        # Process both images
        image2_resized = resizer.process(image2)
        processed_image1 = processor1.process(image1)
        processed_image2 = processor2.process(image2_resized, image1)

        alpha = self.opacity / 100.0  # Opacity as a fraction
        combined_img = cv2.addWeighted(processed_image1, 1 - alpha, processed_image2, alpha, 0)
        cv2.imwrite(self.output_path, combined_img)


def main():
    image_path1 = "image1.png"
    image_path2 = "image2.png"
    output_path = "overlay_image.png"
    opacity_percent = 40  # Example opacity percentage provided by the user

    overlay = ImageOverlay(image_path1, image_path2, output_path, opacity=opacity_percent)

    # Example points for demonstration, replace with your logic to find points
    point1_image2 = (0, 0)
    point2_image2 = (569, 125)
    point2_image1 = (943, 82)
    point1_image1 = (0, 0)
    scale = 2.1313596325862947  # Replace with your scale calculation logic

    resize_processor = ResizeProcessor(scale)
    translate_processor1 = TranslateProcessor(point1_image1[0] - point1_image2[0], point1_image1[1] - point1_image2[1])
    translate_processor2 = TranslateProcessor(point2_image1[0] - point2_image2[0] * scale,
                                              point2_image1[1] - point2_image2[1] * scale)

    overlay.combine_images_with_overlap(translate_processor1, translate_processor2, resize_processor)


if __name__ == "__main__":
    main()
