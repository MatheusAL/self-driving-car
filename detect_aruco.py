import cv2
import numpy as np
import os
import yaml

# referência: https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html


class ArUcoMarkerDetector:
    def __init__(self, frame):
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_1000)
        self.parameters = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.parameters)
        self.image = frame

    def get_parameters_calibration(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(current_directory, "calibration_data.yaml")

        with open(filename, "r") as file:
            data = yaml.safe_load(file)
        camera_matrix = data.get("camera_matrix")
        dist_coeffs = data.get("distortion_coefficients")
        return camera_matrix, dist_coeffs

    def get_coordinates(self, marker_ids, marker_corners):
        marker_id = marker_ids[0]
        marker_length = 0.023
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

        success, rvec, tvec = cv2.solvePnP(
            obj_points,
            marker_corners[0],
            np.array(camera_matrix),
            np.array(dist_coeffs),
            flags=cv2.SOLVEPNP_ITERATIVE,
        )

        print(f"Marker ID: {marker_id}")
        print(f"Rotation Vector (rvec): {rvec}")
        print(f"Translation Vector (tvec): {tvec}")

        return tvec, rvec

    def get_direction_aruco(self, marker_corners, marker_ids):
        tvec, rvec = self.get_coordinates(marker_ids, marker_corners)

        print(f"Camera position: X:{tvec[0]}, Y:{tvec[1]}, and Z:{tvec[2]}")
        print(f"Camera rotation: X:{rvec[0]}, Y:{rvec[1]}, and Z:{rvec[2]}\n")

        rotation_threshold_z = 0.5
        rotation_threshold_xy = 1.5
        threshold_distance = 0.8
        distance_z = 0.15  # distance to stop

        if abs(tvec[2]) > distance_z:
            # se a posição x for negativa -> virar a esquerda, se for positivo -> virar a direita
            if tvec[0] < 0 and abs(rvec[0]) > rotation_threshold_xy and abs(tvec[2]) > rotation_threshold_z:
                return "Left"
            elif tvec[0] > 0 and abs(rvec[0]) > rotation_threshold_xy and abs(tvec[2]) > rotation_threshold_z:
                return "Right"            
            elif (
                abs(tvec[0]) <= threshold_distance
                and abs(tvec[1]) <= threshold_distance
            ):  # se x e y for perto de zero, significa que é só ir pra frente pra chegar no aruco
                return "Forward"
        else:
            return "Parked"

        return "Stop"

    def detect_markers(self):
        image = self.image
        marker_corners, marker_ids, rejected = self.detector.detectMarkers(image)

        if marker_ids is not None:
            return marker_corners, marker_ids
        else:
            print("No ArUco markers detected.")
            return None, None
