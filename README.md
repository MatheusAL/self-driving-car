# Autonomous Car with OpenCV

Computer vision project for creating a self driving car controller by arduino!

## Overview

This project implements an autonomous car using Arduino as the control platform and Python with OpenCV for computer vision tasks. The car utilizes line detection, circle detection, and Aruco marker detection to navigate its environment.

## Features

- **Line Detection**: The car uses computer vision algorithms to detect lines on the road, allowing it to follow a predefined path.

- **Circle Detection (Sign Detection)**: Detects circular objects, specifically designed for recognizing signs on the road.

- **Aruco Marker Detection (Parking)**: Utilizes Aruco markers for precise localization and navigation within the environment, with a focus on parking scenarios.

# How to run?

This code is ready for linux environments. To run the project, follow the steps below:

1. Navigate to the project directory using the command line:

   ```bash
   cd path/to/your/self-driving-car

   ```

2. Install the dependencies

   ```bash
   pip install -r requirements.txt`

   ```

3. Change the camera number according to your system

   ```bash
   # 0 - camera notebook, 1 - camera carrinho(windows), 2 - camera carrinho(linux)
    cap = cv.VideoCapture(2)

   ```

4. Execute serial_cvwaitkey.py

   ```bash
   python3 serial_cvwaitkey.py
   or
   python serial_cvwaitkey.py

   ```

5. For running on Windows, uncomment the line 14 of the class AutonomousCar
