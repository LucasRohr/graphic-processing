''''
2. Utilizar assets/aula7_ruido_sal_pimenta.png e assets/imagem_base_opencv.jpg como
referência sem ruído. Aplicar média 5×5, Gaussiano 5×5 e mediana 5×5 na imagem ruidosa. Salvar os
resultados e, para cada filtro, calcular erro = cv2.absdiff(original, resultado).mean().
Apresentar os três erros no terminal.
'''

from pathlib import Path

import cv2
import numpy as np

entrada_sem_ruido = "assets/imagem_base_opencv.jpg"
entrada_com_ruido = "assets/aula7_ruido_sal_pimenta.png"

# Carrega a imagem sem ruído
imagem_sem_ruido = cv2.imread(entrada_sem_ruido, cv2.IMREAD_GRAYSCALE)
if imagem_sem_ruido is None:
    raise FileNotFoundError(f"Não foi possível abrir: {entrada_sem_ruido}")

# Carrega a imagem com ruído
imagem_com_ruido = cv2.imread(entrada_com_ruido, cv2.IMREAD_GRAYSCALE)
if imagem_com_ruido is None:
    raise FileNotFoundError(f"Não foi possível abrir: {entrada_com_ruido}")

# Aplica filtro de média 5x5
resultado_media = cv2.blur(imagem_com_ruido, (5, 5), borderType=cv2.BORDER_REFLECT_101)
erro_media = cv2.absdiff(imagem_sem_ruido, resultado_media).mean()

# Aplica filtro gaussiano 5x5
resultado_gaussiano = cv2.GaussianBlur(imagem_com_ruido, (5, 5), sigmaX=0, borderType=cv2.BORDER_REFLECT_101)
erro_gaussiano = cv2.absdiff(imagem_sem_ruido, resultado_gaussiano).mean()

# Aplica filtro de mediana 5x5
resultado_mediana = cv2.medianBlur(imagem_com_ruido, 5)
erro_mediana = cv2.absdiff(imagem_sem_ruido, resultado_mediana).mean()

print(f"Erro média: {erro_media}")
print(f"Erro gaussiano: {erro_gaussiano}")
print(f"Erro mediana: {erro_mediana}")

# Salva os resultados em arquivos
pasta_saida = Path("./assets/exercicio_02/")
pasta_saida.mkdir(exist_ok=True)

cv2.imwrite(pasta_saida / "resultado_media.jpg", resultado_media)
cv2.imwrite(pasta_saida / "resultado_gaussiano.jpg", resultado_gaussiano)
cv2.imwrite(pasta_saida / "resultado_mediana.jpg", resultado_mediana)