from pathlib import Path
import cv2
import numpy as np

entrada = Path("assets/imagem_base_opencv.jpg")
pasta_saida = Path("saida")
pasta_saida.mkdir(exist_ok=True)

imagem = cv2.imread(str(entrada))
if imagem is None:
    raise FileNotFoundError(f"Não foi possível abrir: {entrada}")

cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
brilho = cv2.add(cinza, 50)

alpha = 1.5
beta = 128 * (1 - alpha)
contraste = cv2.addWeighted(cinza, alpha, np.zeros_like(cinza), 0, beta)

negativa = cv2.bitwise_not(cinza)
_, binaria = cv2.threshold(cinza, 127, 255, cv2.THRESH_BINARY)

resultados = {
    "01_cinza.png": cinza,
    "02_brilho.png": brilho,
    "03_contraste.png": contraste,
    "04_negativa.png": negativa,
    "05_binaria.png": binaria,
}

for nome, resultado in resultados.items():
    destino = pasta_saida / nome
    if not cv2.imwrite(str(destino), resultado):
        raise OSError(f"Falha ao salvar: {destino}")
    print(nome, resultado.shape, resultado.dtype)
