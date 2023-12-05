import time
import cv2
import serial
import video_capture
from datetime import datetime
import numpy as np
import image_proccess as img
import os

imageProcess = img.ImageProcess()
identified_circle = True
debug_mode = True


def process_image(image):
    cv2.imshow("frame", image)


def get_direction(frame):
    # identified_circle = True  # pra forçar procurar aruco
    direction = imageProcess.process_frame(frame, identified_circle)
    return direction


def get_code_command_car(frame):
    process_image(frame)

    command = get_direction(frame)

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
        return "achou"
    elif command == "20":
        print("Aguardar 20 segundos")
        return "20"
    elif command == "30":
        print("Aguardar 30 segundos")
        return "30"
    elif command == "40":
        print("Aguardar 40 segundos")
        return "40"
    elif command == "50":
        print("Aguardar 50 segundos")
        return "50"


def get_image(index):
    files = sorted(
        os.listdir(
            "/home/matheusl/Área de Trabalho/visao/auto_car/self-driving-car/images/frames_lidos_limpos/"
        )
    )

    # Check if the index is within the valid range
    if 0 <= index < len(files):
        # Construct the full path of the image file
        image_path = os.path.join(
            "/home/matheusl/Área de Trabalho/visao/auto_car/self-driving-car/images/frames_lidos_limpos/",
            files[index],
        )
        # Read the image using OpenCV
        image = cv2.imread(image_path)
        if image is not None:
            return image
        else:
            return None
    else:
        print(
            f"Invalid index: {index}. Index should be in the range [0, {len(files) - 1}]"
        )
        return None


# Define the serial port and baud rate
# ser = serial.Serial("COM5", 9600)
# ser = serial.Serial("/dev/ttyACM0", 9600)  # - linux
# cap = video_capture.connect_camera()
count_stop = 0
index = 50
try:
    while True:
        cv2.waitKey(1)

        if debug_mode == True:
            frame = get_image(index)
            if frame.any() == None:
                exit()
            key = get_code_command_car(frame)

            print("key: " + key)
            index = index + 1
        else:
            print("erro")
            """frame = video_capture.get_frame(cap)
            key = get_code_command_car(frame)

            if key == "w":
                ser.write(b"w")
            elif key == "a":
                ser.write(b"a")
            elif key == "s":
                ser.write(b"s")
            elif key == "d":
                ser.write(b"d")
            elif key == "20":
                time.sleep(20)
                identified_circle = True
            elif key == "30":
                time.sleep(30)
                identified_circle = True
            elif key == "40":
                time.sleep(40)
                identified_circle = True
            elif key == "50":
                time.sleep(50)
                identified_circle = True
            """
            """ if key == ord("q"):
                # Exit the loop when the 'q' key is pressed
                break """

        if cv2.waitKey(1) == ord("q"):
            break

        time.sleep(0.3)  # Add a small delay to avoid rapid key presses (30 fps)

except KeyboardInterrupt:
    pass

# When everything done, release the capture
cap.release()
# Close the serial port and OpenCV window when the program exits
ser.close()
cv2.destroyAllWindows()
