from pathlib import Path
import cv2

caminho = Path("assets/imagem_base_opencv.jpg")
original = cv2.imread(str(caminho))
if original is None:
    raise FileNotFoundError(f"Não foi possível abrir a imagem: {caminho}")
referencia = original
copia = original.copy()
referencia[0:100, 0:100] = [0, 255, 0]
print("referencia é original:", referencia is original)
print("copia é original:", copia is original)
cv2.imshow("Original alterada", original)
cv2.imshow("Copia independente", copia)
cv2.waitKey(0)
cv2.destroyAllWindows()
