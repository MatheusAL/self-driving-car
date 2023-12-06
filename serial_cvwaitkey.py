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
        self.serial_port = serial.Serial('COM5', 9600)
        #self.serial_port = serial.Serial("/dev/ttyACM0", 9600)  # For Linux
        self.video_capture = video_capture.connect_camera()

    def process_image(self, image):
        cv2.imshow("frame", image)

    def get_direction(self, frame):
        direction = self.image_processor.process_frame(frame)
        return direction

    def codeCommand(self, command):
        if command == "Forward":
            print("Movendo para frente.")
            return "w"
        elif command == "Right":
            print("Movendo para direita.")
            return "d"
        elif command == "Left":
            print("Movendo para esquerda.")
            return "a"
        elif command == "backward":
            print("Movendo para trás.")
            return "s"
        elif command == "stop":
            print("Não mover")
            return ""
        elif command in {"20", "30", "40", "50"}:
            print(f"Aguardar {command} segundos")
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
            ):  # geralmente o carrinho vê o aruco já bem próximo da faixa
                break

            key = self.get_code_command_car(frame)

            if key in {"w", "a", "s", "d"}:
                self.serial_port.write(key.encode())

            if key == ord("q") or cv2.waitKey(1) == ord("q"):
                break
            time.sleep(0.3)

    def go_to_aruco(self):
        while True:
            frame = video_capture.get_frame(self.video_capture)
            command = self.image_processor.park_the_car(frame)

            if command == "Parked":
                break

            key = self.codeCommand(command)

            if key in {"w", "a", "s", "d"}:
                self.serial_port.write(key.encode())
                self.serial_port.write(key.encode())
                time.sleep(0.1)
            if key == ord("q") or cv2.waitKey(1) == ord("q"):
                break
            time.sleep(1)

    def run(self):
        try:
            while True:
                #frame = video_capture.get_frame(self.video_capture)
                #key = self.get_code_command_car(frame)
                #if key in {"w", "a", "s", "d"}:
                #    self.serial_port.write(key.encode())
                #elif key in {"20", "30", "40", "50"}:
                    #self.go_to_crosswalk()
                #    time.sleep(int(key))
                self.go_to_aruco()

                #if key == ord("q") or cv2.waitKey(1) == ord("q"):
                #    break

                time.sleep(0.3)  # Add a small delay to avoid rapid key presses (30 fps)

        except KeyboardInterrupt:
            pass

        finally:
            self.video_capture.release()
            self.serial_port.close()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    autonomous_car = AutonomousCar()
    autonomous_car.run()
