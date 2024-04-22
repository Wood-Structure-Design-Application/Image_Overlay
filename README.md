# Image_Overlay Application

This Python application combines two input images by overlaying one image onto the other based on detected points and a calculated scale factor. The application uses OpenCV for image processing tasks.

## Features

- Detect points of a specified color (red or blue by default) in input images
- Calculate the scale factor between the distances of the detected points
- Overlay one image onto the other by applying necessary transformations (resizing and translation)
- Specify the opacity percentage for the overlaid image
- Generate an output image with the combined overlay

## Requirements

- Python 3.x
- OpenCV (cv2)
- NumPy

## Usage

1. Prepare two input images (`image1.png` and `image2.png`) with red and blue points, respectively.
2. Run the `main.py` file.
3. The application will process the input images, detect the points, calculate the scale factor, and overlay the images.
4. The combined image with the overlay will be saved as `overlay_image.png` in the same directory.

You can modify the input image paths, output path, and opacity percentage in the `main.py` file.

## Project Structure

- `Distance.py`: Contains the `PointDistanceCalculator` class for calculating the Euclidean distance between two points.
- `Find_point.py`: Contains the `ColorPointFinder` class for finding points of a specified color in an input image.
- `main.py`: The main file that orchestrates the image combination process and provides an example usage.
- `Overlay.py`: Contains classes for image processing operations (`ResizeProcessor`, `TranslateProcessor`) and the `ImageOverlay` class for combining the images with an overlay.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
