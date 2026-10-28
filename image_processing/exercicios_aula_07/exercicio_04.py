'''
4. Produzir Sobel X, Sobel Y, magnitude do Sobel e Laplaciano. Executar o processamento diretamente
sobre a imagem em tons de cinza e também após um filtro Gaussiano 5×5. Salvar todas as imagens e
comparar a quantidade de pixels com intensidade superior a 100 em cada caso, apresentando as
contagens no terminal.
'''

from pathlib import Path
import cv2
import numpy as np

entrada = "assets/imagem_base_opencv.jpg"

# Carrega
imagem_cinza = cv2.imread(entrada, cv2.IMREAD_GRAYSCALE)
if imagem_cinza is None:
    raise FileNotFoundError(f"Não foi possível abrir: {entrada}")

imagem_gaussiana = cv2.GaussianBlur(
    imagem_cinza, (5, 5), sigmaX=0, borderType=cv2.BORDER_REFLECT_101
)

# Sobel X, Y e magnitude do gradiente

# Aplica o operador de Sobel para calcular a derivada de primeira ordem na direção X
# Isso realça as mudanças abruptas de intensidade no eixo horizontal (detectando contornos verticais)
sobel_x_cinza = cv2.Sobel(
    imagem_cinza, cv2.CV_32F, 1, 0, # dx=1, dy=0 indica que o cálculo é apenas no eixo X
    ksize=3, borderType=cv2.BORDER_REFLECT_101,
)

sobel_x_gaussiana = cv2.Sobel(
    imagem_gaussiana, cv2.CV_32F, 1, 0, # dx=1, dy=0 indica que o cálculo é apenas no eixo X
    ksize=3, borderType=cv2.BORDER_REFLECT_101,
)

# Aplica a mesma lógica matemática, mas agora no eixo Y
# Isso vai realçar as transições de intensidade na vertical (detectando contornos horizontais)
sobel_y_cinza = cv2.Sobel(
    imagem_cinza, cv2.CV_32F, 0, 1, # dx=0, dy=1 indica que o cálculo é apenas no eixo Y
    ksize=3, borderType=cv2.BORDER_REFLECT_101,
)

sobel_y_gaussiana = cv2.Sobel(
    imagem_gaussiana, cv2.CV_32F, 0, 1, # dx=0, dy=1 indica que o cálculo é apenas no eixo Y
    ksize=3, borderType=cv2.BORDER_REFLECT_101,
)

sobel_magnitude_cinza = cv2.magnitude(sobel_x_cinza, sobel_y_cinza)
sobel_magnitude_gaussiana = cv2.magnitude(sobel_x_gaussiana, sobel_y_gaussiana)

visual_sobel_x_cinza = cv2.convertScaleAbs(sobel_x_cinza)
visual_sobel_y_cinza = cv2.convertScaleAbs(sobel_y_cinza)
visual_sobel_magnitude_cinza = cv2.convertScaleAbs(sobel_magnitude_cinza)

visual_sobel_x_gaussiana = cv2.convertScaleAbs(sobel_x_gaussiana)
visual_sobel_y_gaussiana = cv2.convertScaleAbs(sobel_y_gaussiana)
visual_sobel_magnitude_gaussiana = cv2.convertScaleAbs(sobel_magnitude_gaussiana)

# Laplaciano

# Calcula a derivada de segunda ordem da imagem (operador Laplaciano)
# Diferente do Sobel, que detecta contornos em eixos isolados, o Laplaciano é omnidirecional, detectando bordas em todas as direções de uma só vez
laplaciano_cinza = cv2.Laplacian(
    imagem_cinza,                       # 1. Imagem original em tons de cinza
    cv2.CV_32F,                        # 2. Profundidade de saída em ponto flutuante. Fundamental pois a segunda derivada naturalmente gera valores negativos
    ksize=3,                           # 3. Tamanho da matriz do filtro (kernel 3x3)
    borderType=cv2.BORDER_REFLECT_101, # 4. Método de espelhamento para processar os pixels encostados nas bordas da imagem
)

laplaciano_gaussiana = cv2.Laplacian(
    imagem_gaussiana,                  # 1. Imagem com filtro Gaussiano
    cv2.CV_32F,                        # 2. Profundidade de saída em ponto flutuante. Fundamental pois a segunda derivada naturalmente gera valores negativos
    ksize=3,                           # 3. Tamanho da matriz do filtro (kernel 3x3)
    borderType=cv2.BORDER_REFLECT_101, # 4. Método de espelhamento para processar os pixels encostados nas bordas da imagem
)

visual_laplaciano_cinza = cv2.convertScaleAbs(laplaciano_cinza)
visual_laplaciano_gaussiana = cv2.convertScaleAbs(laplaciano_gaussiana)

resultados_imagens = {
    "sobel_x_cinza": visual_sobel_x_cinza,
    "sobel_y_cinza": visual_sobel_y_cinza,
    "sobel_magnitude_cinza": visual_sobel_magnitude_cinza,
    "laplaciano_cinza": visual_laplaciano_cinza,
    "sobel_x_gaussiana": visual_sobel_x_gaussiana,
    "sobel_y_gaussiana": visual_sobel_y_gaussiana,
    "sobel_magnitude_gaussiana": visual_sobel_magnitude_gaussiana,
    "laplaciano_gaussiana": visual_laplaciano_gaussiana,
}

pasta_saida = Path("./assets/exercicio_04/")
pasta_saida.mkdir(exist_ok=True)

for nome, resultado in resultados_imagens.items():
    cv2.imwrite(pasta_saida / f"{nome}.jpg", resultado)

    # Conta a quantidade de pixels com intensidade superior a 100
    contagem_pixels = np.sum(resultado > 100)
    print(f"Quantidade de pixels com intensidade > 100 em {nome}: {contagem_pixels}")