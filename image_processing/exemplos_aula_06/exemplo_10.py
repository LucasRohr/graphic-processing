from pathlib import Path
import cv2

entrada = Path("assets/imagem_base_opencv.jpg")
imagem = cv2.imread(str(entrada), cv2.IMREAD_GRAYSCALE)

if imagem is None:
    raise FileNotFoundError(f"Não foi possível abrir a imagem: {entrada}")

limiar_usado, binaria = cv2.threshold(
    imagem,
    127,
    255,
    cv2.THRESH_BINARY,
)

print("Limiar usado:", limiar_usado)

if not cv2.imwrite("imagem_binaria.png", binaria):
    raise OSError("Falha ao salvar imagem_binaria.png")

cv2.imshow("Tons de cinza", imagem)
cv2.imshow("Binaria", binaria)
cv2.waitKey(0)
cv2.destroyAllWindows()
