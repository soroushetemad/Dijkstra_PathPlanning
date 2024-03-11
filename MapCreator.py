import cv2
import numpy as np
import math

map_width = 1200
map_height = 500

def main():
    WHITE = (130, 120, 230)
    BLACK = (0, 0, 0)
    PADDING_COLOR = (120, 120, 120)
    polygon_sides = 6
    polygon_length = 150
    polygon_bloat = 5
    padding = 5
    border_thickness = 5  # Set the border thickness

    image = np.ones((map_height, map_width, 3), dtype=np.uint8) * WHITE

    # Add a black border around the image
    image[0:border_thickness, :] = BLACK  # Top border
    image[:, 0:border_thickness] = BLACK  # Left border
    image[-border_thickness:, :] = BLACK  # Bottom border
    image[:, -border_thickness:] = BLACK  # Right border

    # # Leftmost rectangle with padding
    cv2.rectangle(image, (100 - padding, 0 - padding), (175 + padding, 400 + padding), BLACK, -1)
    # Rightmost rectangle
    cv2.rectangle(image, (275 - padding, 100 - padding), (350 + padding, 500 + padding), BLACK, -1)
    # Leftmost rectangle
    cv2.rectangle(image, (100, 0), (175, 400), PADDING_COLOR, -1)
    # Rightmost rectangle
    cv2.rectangle(image, (275, 100), (350, 500), PADDING_COLOR, -1)
    polygon_vertices = []
    for i in range(polygon_sides):
        angle = math.radians(i * (360 / polygon_sides) + 90)
        x = 650 + ((polygon_length + polygon_bloat) - padding) * math.cos(angle)
        y = 250 + ((polygon_length + polygon_bloat) - padding) * math.sin(angle)
        polygon_vertices.append((int(x), int(y)))
    cv2.fillPoly(image, [np.array(polygon_vertices)], PADDING_COLOR)
    cv2.polylines(image, [np.array(polygon_vertices)], isClosed=True, color=BLACK, thickness=5)
    # Right vertical part of U with padding
    cv2.rectangle(image, (1020 - padding, 50 - padding), (1100 + padding, 450 + padding), BLACK, -1)
    # Top vertical part of U with padding
    cv2.rectangle(image, (900 - padding, 50 - padding), (1100 + padding, 125 + padding), BLACK, -1)
    # Bottom Horizontal part of U rect with padding
    cv2.rectangle(image, (900 - padding, 375 - padding), (1100 + padding, 450 + padding), BLACK, -1)
    # Right vertical part of U without padding
    cv2.rectangle(image, (1020, 50), (1100, 450), PADDING_COLOR, -1)
    # Top vertical part of U without padding
    cv2.rectangle(image, (900, 50), (1100, 125), PADDING_COLOR, -1)
    cv2.rectangle(image, (900, 375), (1100, 450), PADDING_COLOR, -1)

    cv2.imwrite('output_image.jpg', image)  # Save the image as JPG

if __name__ == "__main__":
    main()
