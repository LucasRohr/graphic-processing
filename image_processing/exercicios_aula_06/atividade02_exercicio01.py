from pathlib import Path
import cv2
import numpy as np

'''
1. Desenvolver um programa que carregue e valide a imagem, exiba largura, altura, número de canais,
dtype e quantidade total de pixels, mostre o valor BGR do pixel central, altere uma região de 100x100
pixels para vermelho e salve o resultado sem modificar o array original.
'''

caminho = Path("./assets/imagem_base_opencv.jpg")
imagem = cv2.imread(str(caminho))

if imagem is None:
    raise FileNotFoundError(f"Não foi possível abrir a imagem: {caminho}")

altura, largura, canais = imagem.shape
total_pixels = altura * largura

print("Dimensões:", imagem.shape)
print("Largura:", largura)
print("Altura:", altura)
print("Número de canais:", canais)
print("Tipo dos dados:", imagem.dtype)
print("Quantidade total de pixels:", total_pixels)

pixel_central = imagem[altura // 2, largura // 2]
print("Valor BGR do pixel central:", pixel_central)

copia_imagem = imagem.copy()
copia_imagem[0:100, 0:100] = [0, 0, 255]  # Alterando a região para vermelho (BGR)

pasta_saida = Path("./assets/exercicio01/")
pasta_saida.mkdir(exist_ok=True)
cv2.imwrite("./assets/exercicio01/imagem_alterada_exercicio01.jpg", copia_imagem)  # Salvando a imagem alterada

cv2.imshow("Imagem Original", imagem)
cv2.imshow("Imagem Alterada", copia_imagem)
cv2.waitKey(0)
cv2.destroyAllWindows()