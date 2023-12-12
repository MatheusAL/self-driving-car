import time
import cv2
import serial
from datetime import datetime
import numpy as np
import video_capture
import image_proccess as img


class AutonomousCar:
    def __init__(self):
        self.image_processor = img.ImageProcess()
        self.identified_circle = False
        ##self.serial_port = serial.Serial("COM5", 9600)
        self.serial_port = serial.Serial("/dev/ttyACM0", 9600)  # For Linux
        self.video_capture = video_capture.connect_camera()

    def process_image(self, image):
        cv2.imshow("frame", image)

    def get_direction(self, frame):
        direction = self.image_processor.process_frame(frame)
        return direction

    def codeCommand(self, command):
        if command == "Forward":
            print("Moving forward")
            return "w"
        elif command == "Right":
            print("Moving right")
            return "d"
        elif command == "Left":
            print("Moving left")
            return "a"
        elif command == "Huge Left":
            print("Moving left - Huge Left")
            return "hugeLeft"
        elif command == "backward":
            print("Moving backward")
            return "s"
        elif command == "stop":
            print("Don't move")
            return ""
        elif command in {"20", "30", "40", "50"}:
            print(f"Wait {command} seconds")
            return command

    def get_code_command_car(self, frame):
        self.process_image(frame)
        command = self.get_direction(frame)
        return self.codeCommand(command)

    def go_to_crosswalk(self):
        while True:
            frame = video_capture.get_frame(self.video_capture)

            if self.image_processor.saw_aruco(
                frame
            ):  # generally the car sees the aruco close to the lane
                break

            key = self.get_code_command_car(frame)

            if key in {"w", "a", "s", "d"}:
                # two controls to give power to the car, one control sometimes it doesn't move
                self.serial_port.write(key.encode())
                self.serial_port.write(key.encode())
                time.sleep(0.4)
            elif key == "hugeLeft":
                # sudden turn - used in situations where the cart does not see both lanes
                self.serial_port.write("a".encode())
                self.serial_port.write("a".encode())
                self.serial_port.write("a".encode())
                self.serial_port.write("a".encode())
                time.sleep(0.5)

            if key == ord("q") or cv2.waitKey(1) == ord("q"):
                break

    def go_to_aruco(self):
        park_distance = 0.15
        step_distance = 0.04
        while True:
            frame = video_capture.get_frame(self.video_capture)
            command, distance = self.image_processor.park_the_car(frame)

            if command == "Parked":
                break

            key = self.codeCommand(command)

            if key in {"w", "a", "s", "d"}:
                # two commannds to give power to the car, one control sometimes it doesn't move
                self.serial_port.write(key.encode())

                if distance > park_distance + step_distance:
                    self.serial_port.write(key.encode())

                # whenever the car turns, it also has to move forward because otherwise the
                # coordinates don't change and it doesn't move
                if (
                    key not in {"w", "s"} and distance > park_distance + step_distance
                ):  # max distance + step distance
                    self.serial_port.write("w".encode())
                    self.serial_port.write("w".encode())

                time.sleep(0.8)

            if key == ord("q") or cv2.waitKey(1) == ord("q"):
                break

            # time.sleep(0.4)

        return "Parked"

    def run(self):
        try:
            while True:
                frame = video_capture.get_frame(self.video_capture)
                key = self.get_code_command_car(frame)
                if key in {"w", "a", "s", "d"}:
                    # two controls to give power to the car, one control sometimes it doesn't move
                    self.serial_port.write(key.encode())
                    self.serial_port.write(key.encode())
                    time.sleep(0.4)
                elif key in {"20", "30", "40", "50"}:
                    self.go_to_crosswalk()
                    time.sleep(int(key))
                    key = self.go_to_aruco()
                elif key == "hugeLeft":
                    # sudden turn - used in situations where the cart does not see both lanes
                    self.serial_port.write("a".encode())
                    self.serial_port.write("a".encode())
                    self.serial_port.write("a".encode())
                    self.serial_port.write("a".encode())
                    time.sleep(0.5)

                if key == "Parked" or key == ord("q") or cv2.waitKey(1) == ord("q"):
                    break

                # time.sleep(0.4)  # Add a small delay to avoid rapid key presses (30 fps)

        except KeyboardInterrupt:
            pass

        finally:
            self.video_capture.release()
            self.serial_port.close()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    autonomous_car = AutonomousCar()
    autonomous_car.run()
