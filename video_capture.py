import numpy as np
import cv2 as cv
import os
import time

frame_count = 0
# cmd = "v4l2-ctl --device 2 --set-ctrl=white_balance_automatic=1,contrast=200,white_balance_temperature=1,focus_automatic_continuous=0"


def connect_camera():
    # 0-camera notebook 1- camera carrinho
    cap = cv.VideoCapture(2)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    fps = 10.0
    height = 720.0
    width = 1280.0

    cap.set(cv.CAP_PROP_FPS, fps)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv.CAP_PROP_AUTOFOCUS, 0)
    cap.set(cv.CAP_PROP_CONTRAST, 200)
    cap.set(cv.CAP_PROP_WHITE_BALANCE_BLUE_U, 1)
    cap.set(cv.CAP_PROP_BUFFERSIZE, 1)
    print(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    print(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    print(cap.get(cv.CAP_PROP_FPS))
    if (
        (cap.get(cv.CAP_PROP_FRAME_WIDTH) != width)
        or (height != cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        or (fps != cap.get(cv.CAP_PROP_FPS))
    ):
        print("ERROR on camera.")
        print(f"Width: {cap.get(cv.CAP_PROP_FRAME_WIDTH)}")
        print(f"Height: {cap.get(cv.CAP_PROP_FRAME_HEIGHT)}")
        print(f"FPS: {cap.get(cv.CAP_PROP_FPS)}")
    else:
        print("Camera OK.")

    return cap


def save_frame(frame):
    global frame_count
    current_directory = os.path.dirname(os.path.abspath(__file__))
    frames_lidos_directory = os.path.join(current_directory, "frames_lidos_limpos")

    if not os.path.exists(frames_lidos_directory):
        os.makedirs(frames_lidos_directory)

    filename = os.path.join(frames_lidos_directory, f"frame_{frame_count}.jpg")
    cv.imwrite(filename, frame)
    frame_count += 1


def get_frame(cap):
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")

    # save_frame(frame)
    return frame
