from pathlib import Path
import cv2

entrada = Path("assets/imagem_base_opencv.jpg")
imagem = cv2.imread(str(entrada), cv2.IMREAD_GRAYSCALE)

if imagem is None:
    raise FileNotFoundError(f"Não foi possível abrir a imagem: {entrada}")

negativa = cv2.bitwise_not(imagem)

if not cv2.imwrite("imagem_negativa.png", negativa):
    raise OSError("Falha ao salvar imagem_negativa.png")

cv2.imshow("Original", imagem)
cv2.imshow("Negativa", negativa)
cv2.waitKey(0)
cv2.destroyAllWindows()
