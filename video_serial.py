import time
import cv2
import serial

# Initialize OpenCV window
cv2.namedWindow("Control")

# Define the serial port and baud rate
ser = serial.Serial('/dev/ttyACM0', 9600)

def process_image ( image ) :
    cv2.imshow('frame', image)

# Change the camera id
cap = cv2.VideoCapture(2)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
# change the resolution and fps to match your device
fps = 10.0
height = 720.0
width = 1280.0

cap.set(cv2.CAP_PROP_FPS, fps)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)


if ( cap.get(cv2.CAP_PROP_FRAME_WIDTH) != width ) or (height != cap.get(cv2.CAP_PROP_FRAME_HEIGHT) ) or ( fps != cap.get(cv2.CAP_PROP_FPS) ) :
    print( "ERRO na configuração da câmera." )
    print( f"Width: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}" )
    print( f"Height: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}" )
    print( f"FPS: {cap.get(cv2.CAP_PROP_FPS)}" )
else :
    print( "Configuração de câmera OK.")

try:
    while True:
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        process_image(frame) 
        key = cv2.waitKey(1) & 0xFF  # Wait for a key press (1ms delay)

        if key == ord('w'):
            ser.write(b'w')
        elif key == ord('a'):
            ser.write(b'a')
        elif key == ord('s'):
            ser.write(b's')
        elif key == ord('d'):
            ser.write(b'd')
        elif key == ord('q'):
            # Exit the loop when the 'q' key is pressed
            break
        time.sleep(0.1)  # Add a small delay to avoid rapid key presses (30 fps)

except KeyboardInterrupt:
    pass

# Close the serial port and OpenCV window when the program exits
ser.close()
cv2.destroyAllWindows()
import time
import cv2
import serial

# Initialize OpenCV window
cv2.namedWindow("Control")

# Define the serial port and baud rate
ser = serial.Serial('/dev/ttyACM0', 9600)

def process_image ( image ) :
    cv2.imshow('frame', image)

# Change the camera id
cap = cv2.VideoCapture(2)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
# change the resolution and fps to match your device
fps = 10.0
height = 720.0
width = 1280.0

cap.set(cv2.CAP_PROP_FPS, fps)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)


if ( cap.get(cv2.CAP_PROP_FRAME_WIDTH) != width ) or (height != cap.get(cv2.CAP_PROP_FRAME_HEIGHT) ) or ( fps != cap.get(cv2.CAP_PROP_FPS) ) :
    print( "ERRO na configuração da câmera." )
    print( f"Width: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}" )
    print( f"Height: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}" )
    print( f"FPS: {cap.get(cv2.CAP_PROP_FPS)}" )
else :
    print( "Configuração de câmera OK.")

try:
    while True:
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        process_image(frame) 
        key = cv2.waitKey(1) & 0xFF  # Wait for a key press (1ms delay)

        if key == ord('w'):
            ser.write(b'w')
        elif key == ord('a'):
            ser.write(b'a')
        elif key == ord('s'):
            ser.write(b's')
        elif key == ord('d'):
            ser.write(b'd')
        elif key == ord('q'):
            # Exit the loop when the 'q' key is pressed
            break
        time.sleep(0.1)  # Add a small delay to avoid rapid key presses (30 fps)

except KeyboardInterrupt:
    pass

# Close the serial port and OpenCV window when the program exits
ser.close()
cv2.destroyAllWindows()
import time
import cv2
import serial

# Initialize OpenCV window
cv2.namedWindow("Control")

# Define the serial port and baud rate
ser = serial.Serial('/dev/ttyACM0', 9600)

def process_image ( image ) :
    cv2.imshow('frame', image)

# Change the camera id
cap = cv2.VideoCapture(2)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
# change the resolution and fps to match your device
fps = 10.0
height = 720.0
width = 1280.0

cap.set(cv2.CAP_PROP_FPS, fps)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)


if ( cap.get(cv2.CAP_PROP_FRAME_WIDTH) != width ) or (height != cap.get(cv2.CAP_PROP_FRAME_HEIGHT) ) or ( fps != cap.get(cv2.CAP_PROP_FPS) ) :
    print( "ERRO na configuração da câmera." )
    print( f"Width: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}" )
    print( f"Height: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}" )
    print( f"FPS: {cap.get(cv2.CAP_PROP_FPS)}" )
else :
    print( "Configuração de câmera OK.")

try:
    while True:
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        process_image(frame) 
        key = cv2.waitKey(1) & 0xFF  # Wait for a key press (1ms delay)

        if key == ord('w'):
            ser.write(b'w')
        elif key == ord('a'):
            ser.write(b'a')
        elif key == ord('s'):
            ser.write(b's')
        elif key == ord('d'):
            ser.write(b'd')
        elif key == ord('q'):
            # Exit the loop when the 'q' key is pressed
            break
        time.sleep(0.1)  # Add a small delay to avoid rapid key presses (30 fps)

except KeyboardInterrupt:
    pass

# Close the serial port and OpenCV window when the program exits
ser.close()
cv2.destroyAllWindows()
