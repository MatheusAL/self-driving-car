import cv2 as cv
import numpy as np
import detect_circle as circle
import os
import detect_aruco as detaruco

# referência detecção de linhas: https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html

frame_count = 0


class ImageProcess:
    def get_central_line(self, image, width):
        height = image.shape[0]
        center_x = width // 2
        line = (center_x, 0, center_x, height)
        return line

    def distance_to_central_line(self, line, center_x):
        x1, y1, x2, y2 = line
        mid_point_x = (x1 + x2) // 2
        return abs(mid_point_x - center_x)

    def calculate_intersection(self, line, central_line):
        x1, y1, x2, y2 = line
        x3, y3, x4, y4 = central_line

        # Calculate the intersection point
        intersection_x = (
            (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
        ) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        intersection_y = (
            (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
        ) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

        return intersection_x, intersection_y

    def get_lines(self, dst):
        linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 100, None, 50, 50)
        number_lines = len(linesP) if linesP is not None else 0
        return linesP

    def get_left_and_right_lines(self, linesP, width):
        linesP = linesP[:, 0, :]

        # Ordena as linhas com base na distância ao centro
        linesP = sorted(
            linesP, key=lambda x: self.distance_to_central_line(x, width // 2)
        )

        # Encontra a linha à esquerda e à direita
        left_line = None
        right_line = None
        maior_esquerda = 0
        maior_x_direita = 0

        for i in range(0, len(linesP)):
            l = linesP[i]
            mid_point_x = (l[0] + l[2]) // 2

            if mid_point_x < width // 2 and l[1] > maior_esquerda:
                maior_esquerda = l[1]

            if mid_point_x > width // 2 and l[1] > maior_x_direita:
                maior_x_direita = l[1]

            # Determina se a linha está à esquerda ou à direita
            if mid_point_x < width // 2:
                side = "Esquerda"
            else:
                side = "Direita"

            # Se a linha estiver à esquerda
            if mid_point_x < width // 2 and l[1] == maior_esquerda:
                left_line = l

            # Se a linha estiver à direita
            elif mid_point_x > width // 2 and l[1] == maior_x_direita:
                right_line = l

        return left_line, right_line

    def draw_left_and_right_lines(self, left_line, right_line, cdstP, width):
        # Desenha as linhas selecionadas
        if left_line is not None:
            cv.line(
                cdstP,
                (left_line[0], left_line[1]),
                (left_line[2], left_line[3]),
                (0, 0, 255),
                3,
                cv.LINE_AA,
            )

        if right_line is not None:
            cv.line(
                cdstP,
                (right_line[0], right_line[1]),
                (right_line[2], right_line[3]),
                (0, 0, 255),
                3,
                cv.LINE_AA,
            )

        self.draw_central_line(cdstP, width)

    def calculate_slope(self, line):
        x1, y1, x2, y2 = line
        return (y2 - y1) / (x2 - x1)

    def get_direction_with_slope(self, left_line, right_line):
        slopeLeft = self.calculate_slope(left_line)
        print("slope da ESQUERDA " + str(slopeLeft))

        slopeRight = self.calculate_slope(right_line)
        print("slope da DIREITA " + str(slopeRight))

        if slopeRight > 0 and slopeRight > 0.15:
            if slopeLeft < 0 and abs(slopeLeft) > 1.5:
                return "Right"
            else:
                return "Forward"
        else:
            if slopeRight < 0 and abs(slopeRight) > 1.5:
                return "Left"
            else:
                return "Right"

    def get_direction_with_intersection_lines(
        self, left_line, right_line, central_line
    ):
        left_intersection_x, left_intercection_y = self.calculate_intersection(
            left_line, central_line
        )

        right_intersection_x, right_intersection_y = self.calculate_intersection(
            right_line, central_line
        )

        y_threshold = 100

        if abs(left_intercection_y - right_intersection_y) <= y_threshold:
            return "Forward"
        elif left_intercection_y > right_intersection_y:
            return "Right"
        else:
            return "Left"

    def get_direction(self, left_line, right_line, central_line):
        if left_line is not None and right_line is None:
            slope = self.calculate_slope(left_line)
            print("slope da ESQUERDA " + str(slope))
            if slope > 0.3:
                return "Huge Left"
            else:
                return "Right"
        elif left_line is None and right_line is not None:
            slope = self.calculate_slope(right_line)
            print("slope da DIREITA " + str(slope))
            if abs(slope) > 0:
                return "Left"
            else:
                return "Right"
        elif left_line is None and right_line is None:
            return "Left"  # se perder as linhas procurar rodando na mesma direção

        # decidir qual das duas opções o carrinho anda melhor
        # get_direction_with_slope --> usa inclinação da linha
        # get_direction_with_intersection_lines --> interseção de duas retas

        # return self.get_direction_with_slope(left_line, right_line)
        return self.get_direction_with_intersection_lines(
            left_line, right_line, central_line
        )

    def get_time_circleframe(self, frame):
        circle_detector = circle.CircleDetector(frame)
        circle_color = circle_detector.detect_circle()

        color_values = {
            "CIANO": 20,
            "MAGENTA": 30,
            "LARANJA": 40,
            "VERDE_CRU": 50,
            "No_color": 0,
        }

        return color_values.get(circle_color, "Cor inválida")

    def saw_aruco(self, frame):
        aruco_manager = detaruco.ArUcoMarkerDetector(frame)
        marker_corners, marker_ids = aruco_manager.detect_markers()

        if marker_corners is not None and marker_ids is not None:
            return True
        else:
            return False

    def park_the_car(self, frame):
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  # Change grayscale
        aruco_manager = detaruco.ArUcoMarkerDetector(frame)
        marker_corners, marker_ids = aruco_manager.detect_markers()
        if marker_corners is not None and marker_ids is not None:
            return aruco_manager.get_direction_aruco(marker_corners, marker_ids)
        else:
            return "Left", 10  # se perder o aruco procurar rodando na mesma direção

    def pre_process_frame(self, frame):
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        lower_blue = np.array([100, 50, 50])
        upper_blue = np.array([130, 255, 255])

        mask = cv.inRange(hsv, lower_blue, upper_blue)

        res = cv.bitwise_and(frame, frame, mask=mask)
        return res

    def process_frame(self, frame):
        direction = "stop"
        time_circle = self.get_time_circleframe(frame)

        if time_circle == 0:
            src = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            if src is None:
                print("Error opening image!")
                return -1

            width = src.shape[1]
            image_blue = self.pre_process_frame(frame)
            dst = cv.Canny(image_blue, 30, 100, None, 3)
            cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
            cdstP = np.copy(cdst)
            linesP = self.get_lines(dst)

            if linesP is not None:
                left_line, right_line = self.get_left_and_right_lines(linesP, width)
                self.draw_left_and_right_lines(left_line, right_line, cdstP, width)
                central_line = self.get_central_line(cdstP, width)
                direction = self.get_direction(left_line, right_line, central_line)
        else:
            direction = str(time_circle)

        return direction

    def draw_central_line(self, image, width):
        height = image.shape[0]
        center_x = width // 2
        image_with_line = cv.line(
            image, (center_x, 0), (center_x, height), (255, 100, 100), 2
        )
        # self.save_frame(image_with_line)

    def save_frame(self, frame):
        global frame_count
        current_directory = os.path.dirname(
            os.path.abspath(__file__)
        )  # Obtém o diretório atual do arquivo em execução
        frames_lidos_directory = os.path.join(
            current_directory, "frames_lidos_processados"
        )  # Constrói o caminho para a pasta 'frames_lidos'

        if not os.path.exists(frames_lidos_directory):
            os.makedirs(
                frames_lidos_directory
            )  # Cria a pasta 'frames_lidos' se não existir

        filename = os.path.join(frames_lidos_directory, f"frame_{frame_count}.jpg")
        cv.imwrite(filename, frame)
        frame_count += 1
