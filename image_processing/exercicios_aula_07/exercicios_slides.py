''''
Aplicação de filtros sobre uma imagem:
1. leitura e validação do arquivo;
2. filtro da média com kernels 3×3 e 7×7;
3. filtro Gaussiano com kernel 7×7;
4. filtro da mediana sobre uma imagem com ruído impulsivo;
5. gradientes Sobel X e Y;
6. magnitude do gradiente;
7. operador Laplaciano;
8. filtro de nitidez com filter2D ;
9. gravação de todas as imagens resultantes.
Cada arquivo deve registrar no nome o filtro e o tamanho do kernel utilizado. 
'''

from pathlib import Path

import cv2
import numpy as np

# 1. leitura e validação do arquivo;

entrada = "assets/imagem_base_opencv.jpg"
# Carrega a imagem descartando as cores para alocar diretamente uma matriz de apenas um canal de intensidade (tons de cinza)
imagem = cv2.imread(entrada, cv2.IMREAD_GRAYSCALE)
if imagem is None:
    raise FileNotFoundError(f"Não foi possível abrir: {entrada}")

# 2. filtro da média com kernels 3×3 e 7×7;

# Aplica um filtro de média (box filter) usando uma janela de 3x3 pixels
# Cada pixel se torna a média aritmética dele mesmo e de seus 8 vizinhos, causando um leve desfoque
media_3x3 = cv2.blur(
    imagem,                            # 1. Imagem original
    (3, 3),                            # 2. Tamanho do kernel (largura, altura). Define a área da vizinhança
    borderType=cv2.BORDER_REFLECT_101, # 3. Estratégia de borda: espelha os pixels da extremidade para calcular os cantos sem erro
)

# Aplica o mesmo algoritmo matematico, mas com uma janela maior de 7x7 pixels
# Como a média agora engloba 49 pixels para cada cálculo, o efeito de desfoque (blur) será bem mais forte
media_7x7 = cv2.blur(
    imagem,
    (7, 7),
    borderType=cv2.BORDER_REFLECT_101,
)

# 3. filtro Gaussiano com kernel 7×7;

# Aplica um filtro passa-baixa Gaussiano para suavizar a imagem
# Diferente do filtro de média, o Gaussiano dá mais peso ao pixel central e menos aos das bordas do kernel, borrando a imagem enquanto preserva melhor os contornos originais
gaussiano = cv2.GaussianBlur(
    imagem,                            # 1. Imagem original
    (7, 7),                            # 2. Tamanho do kernel (largura, altura). Deve ser ímpar
    sigmaX=0,                          # 3. Desvio padrão da curva no eixo X. O valor 0 faz o OpenCV calcular isso automaticamente com base no tamanho do kernel
    borderType=cv2.BORDER_REFLECT_101, # 4. Estratégia de espelhamento para processar os pixels encostados nas beiradas da imagem
)

# 4. filtro da mediana sobre uma imagem com ruído impulsivo;

entrada_mediana = Path("assets/aula7_ruido_sal_pimenta.png")
imagem_ruido = cv2.imread(str(entrada_mediana))

if imagem_ruido is None:
    raise FileNotFoundError(
        f"Não foi possível abrir a imagem: {entrada_mediana}"
    )

mediana = cv2.medianBlur(
    imagem_ruido, # 1. Imagem original
    5,            # 2. Tamanho da janela quadrada (kernel) de 5x5 pixels. Deve ser sempre um número ímpar
)

# 5. gradientes Sobel X e Y;

# Aplica o operador de Sobel para calcular a derivada de primeira ordem na direção X
# Isso realça as mudanças abruptas de intensidade no eixo horizontal (detectando contornos verticais)
sobel_x = cv2.Sobel(
    imagem, cv2.CV_32F, 1, 0, # dx=1, dy=0 indica que o cálculo é apenas no eixo X
    ksize=3, borderType=cv2.BORDER_REFLECT_101,
)

# Aplica a mesma lógica matemática, mas agora no eixo Y
# Isso vai realçar as transições de intensidade na vertical (detectando contornos horizontais)
sobel_y = cv2.Sobel(
    imagem, cv2.CV_32F, 0, 1, # dx=0, dy=1 indica que o cálculo é apenas no eixo Y
    ksize=3, borderType=cv2.BORDER_REFLECT_101,
)

visual_sobel_x = cv2.convertScaleAbs(sobel_x)
visual_sobel_y = cv2.convertScaleAbs(sobel_y)

# 6. magnitude do gradiente;

# Combina as respostas X e Y para calcular a força total do contorno em cada pixel
# Matematicamente, resolve a hipotenusa do triângulo retângulo formado pelas derivadas: sqrt(x² + y²)
magnitude = cv2.magnitude(sobel_x, sobel_y)

visual_sobel_magnitude = cv2.convertScaleAbs(magnitude)

# 7. operador Laplaciano;

# Calcula a derivada de segunda ordem da imagem (operador Laplaciano)
# Diferente do Sobel, que detecta contornos em eixos isolados, o Laplaciano é omnidirecional, detectando bordas em todas as direções de uma só vez
laplaciano = cv2.Laplacian(
    imagem,                            # 1. Imagem original em tons de cinza
    cv2.CV_32F,                        # 2. Profundidade de saída em ponto flutuante. Fundamental pois a segunda derivada naturalmente gera valores negativos
    ksize=3,                           # 3. Tamanho da matriz do filtro (kernel 3x3)
    borderType=cv2.BORDER_REFLECT_101, # 4. Método de espelhamento para processar os pixels encostados nas bordas da imagem
)

# Pega o valor absoluto matemático das derivadas calculadas (transformando números negativos em positivos)
# e converte o resultado de volta para o formato padrão de imagem (inteiros de 0 a 255)
visual_laplaciano = cv2.convertScaleAbs(laplaciano)

# 8. filtro de nitidez com filter2D ;

# Cria uma matriz de convolução (kernel) para realçar a nitidez das bordas (sharpening)
# O valor central alto (5) amplifica a intensidade do pixel atual, enquanto os vizinhos negativos subtraem a intensidade ao redor
# A soma total de todos os elementos da matriz é exatamente 1, o que garante que o brilho global da imagem original seja preservado
kernel = np.array([
    [ 0, -1,  0],
    [-1,  5, -1],
    [ 0, -1,  0],
], dtype=np.float32)

# Aplica o filtro espacial linear passando a nossa matriz personalizada
nitida = cv2.filter2D(
    imagem,                            # 1. Imagem original em tons de cinza ou colorida
    ddepth=-1,                         # 2. Profundidade de dados da saída. O valor negativo forçará a imagem resultante a ter o exato mesmo formato da entrada (ex: inteiro de 8 bits)
    kernel=kernel,                     # 3. A matriz de pesos matemáticos definida acima
    borderType=cv2.BORDER_REFLECT_101, # 4. Estratégia de espelhamento para processar os pixels encostados nas beiradas da imagem
)

# 9. gravação de todas as imagens resultantes.

resultados = {
    "media_3x3.png": media_3x3,
    "media_7x7.png": media_7x7,
    "gaussiano_7x7.png": gaussiano,
    "mediana_5x5.png": mediana,
    "sobel_x.png": visual_sobel_x,
    "sobel_y.png": visual_sobel_y,
    "sobel_magnitude.png": visual_sobel_magnitude,
    "laplaciano.png": visual_laplaciano,
    "nitida.png": nitida,
}

pasta_saida = Path("./assets/exercicios_slides/")
pasta_saida.mkdir(exist_ok=True)

for nome_arquivo, imagem_resultante in resultados.items():
    if not cv2.imwrite(f"./assets/exercicios_slides/{nome_arquivo}", imagem_resultante):
        raise OSError(f"Falha ao salvar {nome_arquivo}")

    print(f"Imagem {nome_arquivo} salva com sucesso.")
    cv2.imshow(nome_arquivo, imagem_resultante)