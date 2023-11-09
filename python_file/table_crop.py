import cv2
import argparse
import numpy as np

class Crop:

    def __init__(self, image)->None:
        self.image = image

    def find_contours(self):
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        thresholded_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        inverted_image = cv2.bitwise_not(thresholded_image)
        dilated_image = cv2.dilate(inverted_image, None, iterations=5)
        contours, _ = cv2.findContours(dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        return contours

    def contours_rectangles(self):
        contours = self.find_contours()
        rectangular_contours = []
        for contour in contours:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            if len(approx) == 4:
                rectangular_contours.append(approx)

        return rectangular_contours

    def area_largest_contour(self):
        max_area = 0
        contour_with_max_area = None
        rectangular_contours = self.contours_rectangles()
        for contour in rectangular_contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                contour_with_max_area = contour
                
        return contour_with_max_area

    def order_points(self, pts):
        
        pts = pts.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")

        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect

    def ordered_contour_points_max_area(self):
    
        contour_max_area = self.area_largest_contour()
        contour_max_area_ordered = self.order_points(contour_max_area)
        image_with_points = self.image.copy()
        for point in contour_max_area_ordered:
            point_coordinates = (int(point[0]), int(point[1]))
            image_with_points = cv2.circle(image_with_points, point_coordinates, 10, (0, 0, 255), -1)
        return contour_max_area_ordered

    def DistanceBetween2Points(self, p1, p2):
        dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
        return dis

    def get_new_width_and_height_of_image(self):
        current_image_width = self.image.shape[1]
        reduced_image = int(current_image_width * 0.9)

        contour_max_area_ordered = self.ordered_contour_points_max_area()
    
        top_left_and_top_right_distance = self.DistanceBetween2Points(
                                            contour_max_area_ordered[0], contour_max_area_ordered[1])
        top_left_and_bottom_left_distance = self.DistanceBetween2Points(
                                            contour_max_area_ordered[0], contour_max_area_ordered[3])

        aspect_ratio = top_left_and_bottom_left_distance / top_left_and_top_right_distance

        new_image_width = reduced_image
        new_image_height = int(new_image_width * aspect_ratio)

        return new_image_width, new_image_height, contour_max_area_ordered


    # def store_process_image(file_name, image):
    #     path = file_name
    #     cv2.imwrite(path, image)
    #     print("Image save")

    def execute(self, file_name):
        # contour_with_max_area_ordered = order_points_in_the_contour_with_max_area(image)
        new_image_width, new_image_height, contour_max_area_ordered = self.get_new_width_and_height_of_image()
        pts1 = np.float32(contour_max_area_ordered)
        pts2 = np.float32([[0, 0], [new_image_width, 0], [new_image_width, new_image_height], [0, new_image_height]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        perspective_corrected_image = cv2.warpPerspective(self.image, matrix, (new_image_width, new_image_height))
        cv2.imwrite(file_name, perspective_corrected_image)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(prog='Crop Image', description='Get the table from the image')
#     parser.add_argument('-i', '--input', type=str, default='table.jpg',
#                         help="Path to save the images")
#     args = parser.parse_args()
#     image = cv2.imread(args.input)
#     print(image.shape)
#     print(type(image))
    # crop_image = Crop(image)
    # crop_image.execute()
    

    