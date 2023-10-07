import time
import cv2
import serial

# Initialize OpenCV window
cv2.namedWindow("Control")

# Define the serial port and baud rate
ser = serial.Serial('/dev/ttyACM0', 9600)

try:
    while True:
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
