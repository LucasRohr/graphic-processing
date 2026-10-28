from pathlib import Path
import cv2

entrada = Path("assets/imagem_base_opencv.jpg")
imagem = cv2.imread(str(entrada), cv2.IMREAD_GRAYSCALE)

if imagem is None:
    raise FileNotFoundError(f"Não foi possível abrir a imagem: {entrada}")

mais_clara = cv2.add(imagem, 50)
mais_escura = cv2.subtract(imagem, 50)

if not cv2.imwrite("brilho_mais_50.png", mais_clara):
    raise OSError("Falha ao salvar brilho_mais_50.png")

if not cv2.imwrite("brilho_menos_50.png", mais_escura):
    raise OSError("Falha ao salvar brilho_menos_50.png")

cv2.imshow("Original", imagem)
cv2.imshow("Mais clara", mais_clara)
cv2.imshow("Mais escura", mais_escura)
cv2.waitKey(0)
cv2.destroyAllWindows()
