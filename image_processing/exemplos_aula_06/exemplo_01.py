from pathlib import Path
import cv2

caminho = Path("./assets/imagem_base_opencv.jpg")
imagem = cv2.imread(str(caminho))
if imagem is None:
    raise FileNotFoundError(f"Não foi possível abrir a imagem: {caminho}")
print("Dimensões:", imagem.shape)
print("Tipo dos dados:", imagem.dtype)
cv2.imshow("Imagem original", imagem)
cv2.waitKey(0)
cv2.destroyAllWindows()
