from pathlib import Path
import cv2

caminho = Path("assets/imagem_base_opencv.jpg")
imagem = cv2.imread(str(caminho))

if imagem is None:
    raise FileNotFoundError(f"Não foi possível abrir a imagem: {caminho}")

resultado = imagem.copy()

# Linhas de 50 a 149 e colunas de 50 a 249
resultado[50:150, 50:250] = [0, 255, 0]

cv2.imshow("Original", imagem)
cv2.imshow("Regiao alterada", resultado)
cv2.waitKey(0)
cv2.destroyAllWindows()
