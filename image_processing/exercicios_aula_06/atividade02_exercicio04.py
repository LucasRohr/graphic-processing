from pathlib import Path
import cv2
import numpy as np

'''
4. Recortar o cartão com a palavra “OpenCV” com cartao = imagem[370:640, 430:860]. Converter o
recorte para tons de cinza, aumentar o contraste, produzir uma versão binária e salvar o recorte original
e as três versões processadas.
'''

caminho = Path("./assets/imagem_base_opencv.jpg")
imagem = cv2.imread(str(caminho))

if imagem is None:
    raise FileNotFoundError(f"Não foi possível abrir a imagem: {caminho}")

cartao = imagem[370:640, 430:860]

cartao_cinza = cv2.cvtColor(cartao, cv2.COLOR_BGR2GRAY)

alpha = 3
beta = 128 * (1 - alpha)

cartao_contraste_aumentado = cv2.addWeighted(
    cartao_cinza,
    alpha,
    np.zeros_like(cartao_cinza),
    0,
    beta,
)

cartao_binario = cv2.threshold(
    cartao_cinza,
    127,
    255,
    cv2.THRESH_BINARY,
)[1]

pasta_saida = Path("./assets/exercicio04/")
pasta_saida.mkdir(exist_ok=True)

imagens = {
    "original": cartao,
    "cinza": cartao_cinza,
    "contraste_aumentado": cartao_contraste_aumentado,
    "binario": cartao_binario,
}

for nome, img in imagens.items():
    cv2.imwrite(f"./assets/exercicio04/cartao_{nome}_exercicio04.jpg", img)
    print(f"{nome} salvo em ./assets/exercicio04/cartao_{nome}_exercicio04.jpg")