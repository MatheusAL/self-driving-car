import numpy as np
import cv2 as cv
from datetime import datetime


def process_image ( image ) :
    cv.imshow('frame', image)

# Change the camera id
cap = cv.VideoCapture(2)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# change the resolution and fps to match your device
fps = 10.0
height = 720.0
width = 1280.0

cap.set(cv.CAP_PROP_FPS, fps)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
cap.set(cv.CAP_PROP_FRAME_WIDTH, width)


if ( cap.get(cv.CAP_PROP_FRAME_WIDTH) != width ) or (height != cap.get(cv.CAP_PROP_FRAME_HEIGHT) ) or ( fps != cap.get(cv.CAP_PROP_FPS) ) :
    print( "ERRO na configuração da câmera." )
    print( f"Width: {cap.get(cv.CAP_PROP_FRAME_WIDTH)}" )
    print( f"Height: {cap.get(cv.CAP_PROP_FRAME_HEIGHT)}" )
    print( f"FPS: {cap.get(cv.CAP_PROP_FPS)}" )
else :
    print( "Configuração de câmera OK.")


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    process_image(frame) 

    print(datetime.utcnow().strftime('%F %T.%f')[:-3])
    
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

