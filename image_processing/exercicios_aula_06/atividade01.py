from pathlib import Path
import cv2
import numpy as np

# Exercicio 01 (slides)

# 1. carregar e validar o arquivo;
caminho = Path("./assets/house.jpg")
imagem = cv2.imread(str(caminho))

if imagem is None:
    raise FileNotFoundError(f"Não foi possível abrir a imagem: {caminho}")

# 2. imprimir shape e dtype ;
print("Dimensões:", imagem.shape)
print("Tipo dos dados:", imagem.dtype)
cv2.imshow("Imagem original", imagem)

# 3. gerar uma versão em tons de cinza;
cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
print("Dimensões da imagem em tons de cinza:", cinza.shape)
print("Tipo dos dados da imagem em tons de cinza:", cinza.dtype)
cv2.imshow("Imagem em tons de cinza", cinza)

# 4. gerar uma versão com brilho alterado;
brilho = cv2.add(cinza, 50)
cv2.imshow("Imagem com brilho alterado", brilho)

# 5. gerar uma versão com contraste alterado;
alpha = 1.5
beta = 128 * (1 - alpha)

contraste = cv2.addWeighted(
    cinza,
    alpha,
    np.zeros_like(cinza),
    0,
    beta,
)
cv2.imshow("Imagem com contraste alterado", contraste)

# 6. gerar uma versão negativa;
negativa = cv2.bitwise_not(cinza)
cv2.imshow("Imagem negativa", negativa)

# 7. gerar uma versão binária;
limiar_usado, binaria = cv2.threshold(
    cinza,
    127,
    255,
    cv2.THRESH_BINARY,
)
cv2.imshow("Imagem binária", binaria)

# 8. salvar todas as saídas em uma pasta.
pasta_saida = Path("./assets/saidas_house/")
pasta_saida.mkdir(exist_ok=True)

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