import cv2.aruco as aruco
import cv2
import numpy as np
import yaml

# referência: https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html


class ArUcoMarkerDetector:
    def __init__(self, frame):
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
        self.parameters = aruco.DetectorParameters()
        self.detector = aruco.ArucoDetector(self.aruco_dict, self.parameters)
        self.image = frame

    def get_parameters_calibration(self):
        #filename = "/home/matheusl/Área de Trabalho/visao/self-driving/self-driving-car/implementacao-20231202T133008Z-001/implementacao/calibration_data.yaml"
        filename = "C:/Users/Juliana/Desktop/mestrado/DPI/INF-492 Fundamentos Visao Computacional/TrabalhoFinal_CarrinhoRobo/codigo/carrinho_autonomo_novo/calibration_data"

        with open(filename, "r") as file:
            data = yaml.safe_load(file)
        camera_matrix = data.get("camera_matrix")
        dist_coeffs = data.get("distortion_coefficients")
        return camera_matrix, dist_coeffs

    def get_coordinates(self, marker_ids, marker_corners):
        marker_id = marker_ids[0]
        marker_length = 0.05
        camera_matrix, dist_coeffs = self.get_parameters_calibration()

        # Set coordinate system
        obj_points = np.array(
            [
                [-marker_length / 2, marker_length / 2, 0],
                [marker_length / 2, marker_length / 2, 0],
                [marker_length / 2, -marker_length / 2, 0],
                [-marker_length / 2, -marker_length / 2, 0],
            ],
            dtype=np.float32,
        ).reshape(-1, 3, 1)
        # obj_points = np.zeros((4, 1, 3), dtype=np.float32)
        # Verifique se há pelo menos 4 pontos correspondentes
        # if len(marker_corners[0]) >= 4:
        success, rvec, tvec = cv2.solvePnP(
            obj_points,
            marker_corners[0],
            np.array(camera_matrix),
            np.array(dist_coeffs),
            flags=cv2.SOLVEPNP_ITERATIVE,
        )
        # Restante do seu código
        # else:
        #    print("Não há pontos suficientes para calcular a pose.")

        # rvec, tvec, _ = aruco.estimatePoseSingleMarkers(
        #    marker_corners[0][0], 1, camera_matrix, dist_coeffs
        # )
        print(f"Marker ID: {marker_id}")
        print(f"Rotation Vector (rvec): {rvec}")
        print(f"Translation Vector (tvec): {tvec}")

        return tvec, rvec

    def get_direction_aruco(self, marker_corners, marker_ids):
        tvec, rvec = self.get_coordinates(marker_ids, marker_corners)

        print(f"Camera position: X:{tvec[0]}, Y:{tvec[1]}, and Z:{tvec[2]}")
        print(f"Camera rotation: X:{rvec[0]}, Y:{rvec[1]}, and Z:{rvec[2]}\n")

        # first try
        rotation_threshold = 0.4
        threshold_distance = 0.5
        return "Stop"
        if tvec[2] > threshold_distance:
            if abs(rvec[2]) < rotation_threshold:
                return "Forward"
            elif rvec[2] > 0:
                return "Left"
            else:
                return "Right"

        return "Stop"

    def detect_markers(self):
        image = self.image
        marker_corners, marker_ids, rejected = self.detector.detectMarkers(image)

        if marker_ids is not None:
            return marker_corners, marker_ids
        else:
            print("No ArUco markers detected.")
            return None