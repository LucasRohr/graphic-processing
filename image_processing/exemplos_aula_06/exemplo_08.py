from pathlib import Path
import cv2
import numpy as np

entrada = Path("assets/imagem_base_opencv.jpg")
imagem = cv2.imread(str(entrada), cv2.IMREAD_GRAYSCALE)

if imagem is None:
    raise FileNotFoundError(f"Não foi possível abrir a imagem: {entrada}")

alpha = 1.5
beta = 128 * (1 - alpha)

contraste = cv2.addWeighted(
    imagem,
    alpha,
    np.zeros_like(imagem),
    0,
    beta,
)

if not cv2.imwrite("contraste.png", contraste):
    raise OSError("Falha ao salvar contraste.png")

cv2.imshow("Original", imagem)
cv2.imshow("Contraste", contraste)
cv2.waitKey(0)
cv2.destroyAllWindows()
