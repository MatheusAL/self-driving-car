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

        print(f"Line: ({x1}, {y1}), ({x2}, {y2})")
        print(f"Central Line: ({x3}, {y3}), ({x4}, {y4})")

        # Calculate the intersection point
        intersection_x = (
            (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
        ) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        intersection_y = (
            (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
        ) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

        return intersection_x, intersection_y

    def get_lines(self, dst):
        linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 100, None, 50, 200)
        number_lines = len(linesP) if linesP is not None else 0
        print(f"Número de linhas encontradas: {number_lines}")
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

            # Imprime informações sobre a linha, incluindo a posição em relação ao centro
            print(
                f"Linha {i + 1}: Pontos iniciais ({l[0]}, {l[1]}), Pontos finais ({l[2]}, {l[3]}), Posição: {side}"
            )

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
            print(
                f"Linha à esquerda: Pontos iniciais ({left_line[0]}, {left_line[1]}), Pontos finais ({left_line[2]}, {left_line[3]})"
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
            print(
                f"Linha à direita: Pontos iniciais ({right_line[0]}, {right_line[1]}), Pontos finais ({right_line[2]}, {right_line[3]})"
            )

        self.draw_central_line(cdstP, width)

    def get_direction(self, left_line, right_line, central_line):
        left_intersection_x, left_intercection_y = self.calculate_intersection(
            left_line, central_line
        )
        print(f"Intersection_left: ({left_intersection_x}, {left_intercection_y})")

        right_intersection_x, right_intersection_y = self.calculate_intersection(
            right_line, central_line
        )
        print(f"Intersection_right: ({right_intersection_x}, {right_intersection_y})")

        y_threshold = 100

        if abs(left_intercection_y - right_intersection_y) <= y_threshold:
            return "Forward"
        elif left_intercection_y < right_intersection_y:
            return "Right"
        else:
            return "Left"

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

    def process_frame(self, frame, identified_circle):
        if identified_circle:
            aruco_manager = detaruco.ArUcoMarkerDetector(frame)
            try:
                marker_corners, marker_ids = aruco_manager.detect_markers()

                if marker_corners is not None and marker_ids is not None:
                    direction = aruco_manager.get_direction_aruco(
                        marker_corners, marker_ids
                    )
                else:
                    direction = "stop"

            except:
                direction = "Left"
                # turn right 4 times
                # turn left 4 times

        else:
            direction = "stop"
            time_circle = self.get_time_circleframe(frame)

            if time_circle == 0:
                src = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                if src is None:
                    print("Error opening image!")
                    return -1

                width = src.shape[1]
                dst = cv.Canny(src, 30, 100, None, 3)
                cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
                cdstP = np.copy(cdst)
                linesP = self.get_lines(dst)

                if linesP is not None:
                    left_line, right_line = self.get_left_and_right_lines(linesP, width)
                    self.draw_left_and_right_lines(left_line, right_line, cdstP, width)

                    if left_line is not None and right_line is not None:
                        central_line = self.get_central_line(cdstP, width)
                        direction = self.get_direction(
                            left_line, right_line, central_line
                        )
            else:
                direction = str(time_circle)

        return direction

    def draw_central_line(self, image, width):
        height = image.shape[0]
        center_x = width // 2
        image_with_line = cv.line(
            image, (center_x, 0), (center_x, height), (255, 100, 100), 2
        )
        self.save_frame(image_with_line)

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
