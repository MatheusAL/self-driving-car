import cv2
import numpy as np

# referência: https://docs.opencv.org/4.x/da/d53/tutorial_py_houghcircles.html


class CircleDetector:
    def __init__(self, image):
        self.image = image

    def detect_color(self, color_at_center_rgb):
        r, g, b = color_at_center_rgb

        if 0 <= r <= 20 and 45 <= g <= 255 and 70 <= b <= 255 and g <= b:
            return "CIANO"
        elif 190 <= r <= 255 and 0 <= g <= 60 and 35 <= b <= 255:
            return "MAGENTA"
        elif 190 <= r <= 255 and 80 <= g <= 165 and 0 <= b <= 20:
            return "LARANJA"
        elif 0 <= r <= 110 and 95 <= g <= 255 and 0 <= b <= 190 and g > b:
            return "VERDE_CRU"
        else:
            return "No_color"

    def detect_circle(self):
        img = self.image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)

        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT_ALT,
            dp=1,
            minDist=20,
            param1=50,
            param2=0.5,
            minRadius=40,
            maxRadius=45
        )

        if circles is not None:
            circles = np.uint16(np.around(circles))
            reference_point = (100, 100)
            min_distance = float("inf")
            nearest_circle_index = None

            for i, circle in enumerate(circles[0, :]):
                distance = np.linalg.norm(circle[:2] - reference_point)

                if distance < min_distance:
                    min_distance = distance
                    nearest_circle_index = i

            if nearest_circle_index is not None:
                nearest_circle = circles[0, nearest_circle_index]
                center_x, center_y = nearest_circle[0], nearest_circle[1]

                cv2.circle(img, (center_x, center_y), nearest_circle[2], (0, 255, 0), 2)

                color_at_center = img[center_y, center_x]
                color_at_center_rgb = color_at_center[::-1]

                print(f"Círculo mais próximo: {nearest_circle}")
                print(f"Cor do círculo mais próximo RGB: {color_at_center_rgb}")

                color_name = self.detect_color(color_at_center_rgb)
                # cv2.imshow("Círculo mais próximo", img)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
        else:
            print("Nenhum círculo foi detectado.")
            color_name = "No_color"

        return color_name
