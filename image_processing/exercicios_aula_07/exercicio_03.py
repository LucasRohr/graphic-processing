''''
3. Aplicar com cv2.filter2D os kernels de nitidez, detecção de contornos e relevo abaixo. Salvar os
resultados, imprimir a soma dos pesos de cada kernel e explicar em comentários como essa soma
influencia regiões de intensidade constante.

Nitidez:

[[ 0, -1, 0],
[-1, 5, -1],
[ 0, -1, 0]]

Detecção de contornos:

[[-1, -1, -1],
[-1, 8, -1],
[-1, -1, -1]]

Relevo:

[[-2, -1, 0],
[-1, 1, 1],
[ 0, 1, 2]]
'''

from pathlib import Path
import cv2
import numpy as np

entrada = "assets/imagem_base_opencv.jpg"

# Carrega
imagem = cv2.imread(entrada, cv2.IMREAD_GRAYSCALE)
if imagem is None:
    raise FileNotFoundError(f"Não foi possível abrir: {entrada}")

# Executa filtragem com kernel da nitidez
kernel_nitidez = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)

resultado_nitidez = cv2.filter2D(
    imagem,
    # Mantém o tipo de dado da matriz de saída idêntico ao da original (inteiros de 8 bits)
    ddepth=-1,
    kernel=kernel_nitidez,
    # Define a matemática para calcular os pixels que ficam nas extremidades da foto
    # BORDER_REFLECT_101 espelha os valores internos como um reflexo de espelho no limite da imagem, evitando bordas pretas falsas
    borderType=cv2.BORDER_REFLECT_101,
)

# Executa filtragem com kernel de detecção de contornos
kernel_contornos = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=np.float32)

resultado_contornos = cv2.filter2D(
    imagem,
    # Mantém o tipo de dado da matriz de saída idêntico ao da original (inteiros de 8 bits)
    ddepth=-1,
    kernel=kernel_contornos,
    # Define a matemática para calcular os pixels que ficam nas extremidades da foto
    # BORDER_REFLECT_101 espelha os valores internos como um reflexo de espelho no limite da imagem, evitando bordas pretas falsas
    borderType=cv2.BORDER_REFLECT_101,
)

# Executa filtragem com kernel de relevo
kernel_relevo = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]], dtype=np.float32)

resultado_relevo = cv2.filter2D(
    imagem,
    # Mantém o tipo de dado da matriz de saída idêntico ao da original (inteiros de 8 bits)
    ddepth=-1,
    kernel=kernel_relevo,
    # Define a matemática para calcular os pixels que ficam nas extremidades da foto
    # BORDER_REFLECT_101 espelha os valores internos como um reflexo de espelho no limite da imagem, evitando bordas pretas falsas
    borderType=cv2.BORDER_REFLECT_101,
)

# Salva os resultados em arquivos
pasta_saida = Path("./assets/exercicio_03/")
pasta_saida.mkdir(exist_ok=True)

cv2.imwrite(pasta_saida / "resultado_nitidez.jpg", resultado_nitidez)
cv2.imwrite(pasta_saida / "resultado_contornos.jpg", resultado_contornos)
cv2.imwrite(pasta_saida / "resultado_relevo.jpg", resultado_relevo)

# Imprime a soma dos pesos de cada kernel
soma_nitidez = np.sum(kernel_nitidez)
soma_contornos = np.sum(kernel_contornos)
soma_relevo = np.sum(kernel_relevo)

print(f"Soma dos pesos do kernel de nitidez: {soma_nitidez}")
print(f"Soma dos pesos do kernel de detecção de contornos: {soma_contornos}")
print(f"Soma dos pesos do kernel de relevo: {soma_relevo}")

# Explicação:
# A soma dos pesos de um kernel influencia como ele reage a regiões de intensidade constante na imagem. 
# - Se a soma dos pesos for igual a 1, o kernel preserva a intensidade média da região, resultando em uma imagem filtrada que mantém o brilho geral.
# - Se a soma dos pesos for maior que 1, o kernel amplifica a intensidade da região, tornando-a mais brilhante.
# - Se a soma dos pesos for menor que 1, o kernel reduz a intensidade da região, tornando-a mais escura.
# - Se a soma dos pesos for igual a 0, o kernel realça as diferenças de intensidade, destacando bordas e contornos,
#   enquanto regiões de intensidade constante tendem a se tornar neutras (cinza médio)