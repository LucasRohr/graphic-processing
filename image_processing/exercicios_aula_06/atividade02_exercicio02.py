from pathlib import Path
import cv2
import numpy as np

'''
2. A partir da imagem original, gerar versões em tons de cinza, com brilho aumentado, com brilho
reduzido, com contraste aumentado e negativa. Salvar cada resultado com nome que identifique a
operação. Imprimir shape e dtype de cada imagem gerada.
'''

caminho = Path("./assets/imagem_base_opencv.jpg")
imagem = cv2.imread(str(caminho))

if imagem is None:
    raise FileNotFoundError(f"Não foi possível abrir a imagem: {caminho}")

# Convertendo para tons de cinza
imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

# Aumentando o brilho
imagem_brilho_aumentado = cv2.add(imagem, 50)

# Reduzindo o brilho
imagem_brilho_reduzido = cv2.subtract(imagem, 50)

# Aumentando o contraste
alpha = 3
beta = 128 * (1 - alpha)

imagem_contraste_aumentado = cv2.addWeighted(
    imagem,
    alpha,
    np.zeros_like(imagem),
    0,
    beta,
)

# Negativa da imagem
imagem_negativa = cv2.bitwise_not(imagem)

imagens = {
    "cinza": imagem_cinza,
    "brilho_aumentado": imagem_brilho_aumentado,
    "brilho_reduzido": imagem_brilho_reduzido,
    "contraste_aumentado": imagem_contraste_aumentado,
    "negativa": imagem_negativa,
}

pasta_saida = Path("./assets/exercicio02/")
pasta_saida.mkdir(exist_ok=True)

for nome, img in imagens.items():
    print(f"{nome} - Dimensões: {img.shape}, Tipo dos dados: {img.dtype}")
    cv2.imwrite(f"./assets/exercicio02/imagem_{nome}_exercicio02.jpg", img)
