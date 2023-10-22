import cv2
import numpy as np
import matplotlib.pyplot as plt

# Substitua 'caminho_completo_para_pista.jpg' pelo caminho completo da sua imagem
caminho_imagem_pista = (
    "/home/matheusl/Área de Trabalho/visao/self-driving/self-driving-car/images/1.jpeg"
)

# Carregue a imagem da pista
imagem_pista = cv2.imread(caminho_imagem_pista, cv2.IMREAD_GRAYSCALE)


def cut_image(image):
    return image[150:500, :]


def sharp_cut_image(image):
    return image[:, 0:1525]


def getROI(image):
    height = image.shape[0]
    width = image.shape[1]
    # Defining Triangular ROI: The values will change as per your camera mounts
    triangle = np.array([[(0, 300), (400, 50), (2500, 300)]])
    # creating black image same as that of input image
    black_image = np.zeros_like(image)
    mask = cv2.fillPoly(black_image, triangle, color=(255, 0, 0))
    # applying mask on original image
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image


if imagem_pista is None:
    print("Erro ao carregar a imagem.")
else:
    # Aplicar o detector de bordas Canny

    imagem_pista = cut_image(imagem_pista)
    bordas = cv2.Canny(imagem_pista, threshold1=50, threshold2=150)

    # Encontre os contornos das bordas
    contornos, _ = cv2.findContours(bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    roi = getROI(bordas)
    lines = cv2.HoughLinesP(
        roi,
        1,
        np.pi / 180,
        100,
        np.array([]),
        minLineLength=100,
        maxLineGap=100000,
    )
    line_image = display_lines(imagem_pista, lines)
    cv2.imshow("Result", display_lines(line_image, lines))

    img = sharp_cut_image(line_image)
    # Calculate the middle point of the road
    if lines is not None and len(lines) >= 2:
        left_line = lines[0][0]
        right_line = lines[1][0]

        # Calculate the middle point as the intersection of the left and right lines
        middle_x = (left_line[2] + right_line[0]) // 2
        middle_y = (left_line[1] + right_line[1]) // 2

        middlex2 = (left_line[2] + right_line[0]) // 2
        middley2 = (left_line[2] + right_line[2]) // 2
        # Draw a line representing the middle of the road
        cv2.line(
            img,
            (middle_x, middle_y),
            (middlex2, middley2),
            (255, 255, 255),
            5,
        )
        # Assuming the car's position is in the center of the image
        car_x = img.shape[1] // 2
        car_y = img.shape[
            0
        ]  # Adjust as needed based on the car's position in your image

        # Define a margin of error (e.g., 10 pixels)
        margin_of_error = 150

        # Calculate the boundaries of the central region
        center_start = car_x - margin_of_error
        center_end = car_x + margin_of_error

        # Determine if the car is within the central region
        if center_start <= middle_x <= center_end:
            print("Car is in the central region of the road.")
        else:
            # Car is outside the central region, so adjust the car's direction (e.g., go forward)
            print(
                "Car is outside the central region. Adjust the car's direction (e.g., go forward)."
            )
    else:
        print("No lines detected.")


cv2.waitKey(0)
