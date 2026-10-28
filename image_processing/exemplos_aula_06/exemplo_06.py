from pathlib import Path
import cv2

entrada = Path("assets/imagem_base_opencv.jpg")
saida = Path("imagem_cinza.png")
imagem = cv2.imread(str(entrada))
if imagem is None:
    raise FileNotFoundError(f"Não foi possível abrir a imagem: {entrada}")
cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
if not cv2.imwrite(str(saida), cinza):
    raise OSError(f"Não foi possível salvar: {saida}")
print("Colorida:", imagem.shape, imagem.dtype)
print("Cinza:", cinza.shape, cinza.dtype)
cv2.imshow("Colorida", imagem)
cv2.imshow("Tons de cinza", cinza)
cv2.waitKey(0)
cv2.destroyAllWindows()
