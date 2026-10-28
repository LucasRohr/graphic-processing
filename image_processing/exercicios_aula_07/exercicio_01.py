''''
1. Selecionar uma região de no máximo 150×150 pixels de uma imagem em tons de cinza. Implementar
manualmente um filtro da média 3×3 com tratamento de borda por reflexão, laços sobre a imagem e o
kernel, acumulador em ponto flutuante e saturação entre 0 e 255. Comparar o resultado com cv2.blur
e imprimir a maior diferença entre as duas imagens.
'''

from pathlib import Path

import cv2
import numpy as np

def media_manual(imagem, kernel):
    altura_k, largura_k = kernel.shape
    
    # Garante que a matriz do filtro tenha um pixel central exato (ex: 3x3, 5x5)
    if altura_k % 2 == 0 or largura_k % 2 == 0:
        raise ValueError("O kernel deve ter dimensões ímpares.")

    # Calcula quantos pixels o kernel se estende a partir do centro
    raio_y = altura_k // 2
    raio_x = largura_k // 2
    
    # Adiciona uma margem espelhada ao redor da imagem
    # Isso evita erro de "out of bounds" ao aplicar o kernel nos pixels das beiradas
    borda = cv2.copyMakeBorder(
        imagem, raio_y, raio_y, raio_x, raio_x,
        cv2.BORDER_REFLECT_101,
    )
    
    # Matriz vazia para armazenar o resultado temporário com precisão decimal
    saida = np.zeros(imagem.shape, dtype=np.float32)

    # Percorre cada pixel da imagem original (janela deslizante)
    for y in range(imagem.shape[0]):
        for x in range(imagem.shape[1]):
            soma = 0.0
            
            # Sobrepõe o kernel na região atual e faz a soma ponderada
            for ky in range(altura_k):
                for kx in range(largura_k):
                    pixel = float(borda[y + ky, x + kx])
                    peso = float(kernel[ky, kx])
                    soma += pixel * peso
                    
            # Grava o resultado matemático no pixel central da janela
            saida[y, x] = soma

    # Corta os valores que extrapolaram 0-255 e converte de volta para formato de imagem (inteiro 8 bits)
    return np.clip(saida, 0, 255).astype(np.uint8)

entrada = "assets/imagem_base_opencv.jpg"
# Carrega a imagem descartando as cores para alocar diretamente uma matriz de apenas um canal de intensidade (tons de cinza)
imagem = cv2.imread(entrada, cv2.IMREAD_GRAYSCALE)
if imagem is None:
    raise FileNotFoundError(f"Não foi possível abrir: {entrada}")

regiao = imagem[370:520, 430:580]  # Seleciona uma região de 150x150 pixels

resultado_manual = media_manual(regiao, np.full((3, 3), 1 / 9, dtype=np.float32))
resultado_cv2 = cv2.blur(regiao, (3, 3), borderType=cv2.BORDER_REFLECT_101)

# Calcula a diferença absoluta entre as duas imagens resultantes
diferenca = cv2.absdiff(resultado_manual, resultado_cv2)
maior_diferenca = np.max(diferenca)

print(f"Maior diferença entre o filtro manual e cv2.blur: {maior_diferenca}")

pasta_saida = Path("./assets/exercicio_01/")
pasta_saida.mkdir(exist_ok=True)

cv2.imwrite(str(pasta_saida / "resultado_manual.png"), resultado_manual)
cv2.imwrite(str(pasta_saida / "resultado_cv2.png"), resultado_cv2)

cv2.imshow("Região Original", regiao)
cv2.imshow("Resultado Manual", resultado_manual)
cv2.imshow("Resultado cv2.blur", resultado_cv2)
cv2.waitKey(0)
cv2.destroyAllWindows()
