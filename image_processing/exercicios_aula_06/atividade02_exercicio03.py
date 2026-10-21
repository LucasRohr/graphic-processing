from pathlib import Path
import cv2
import numpy as np

'''
3. Converter a imagem para tons de cinza e aplicar limiarização com os valores 80, 127 e 180. Salvar os
três resultados, contar quantos pixels ficaram brancos em cada um, apresentar no terminal a
porcentagem de pixels brancos e registrar em comentário no código qual limiar separou melhor o texto
do cartão.
'''

# Resultado:
'''
O limiar de 180 separou melhor o texto do cartão, pois manteve a maior parte do texto legível e eliminou a maioria dos ruídos de fundo.
'''

caminho = Path("./assets/imagem_base_opencv.jpg")
imagem = cv2.imread(str(caminho))

if imagem is None:
    raise FileNotFoundError(f"Não foi possível abrir a imagem: {caminho}")

imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

limiares = [80, 127, 180]

pasta_saida = Path("./assets/exercicio03/")
pasta_saida.mkdir(exist_ok=True)

for limiar in limiares:
    limiar_usado, binaria = cv2.threshold(
        imagem_cinza,
        limiar,
        255,
        cv2.THRESH_BINARY,
    )

    total_pixels = binaria.size
    pixels_brancos = np.count_nonzero(binaria == 255)
    porcentagem_brancos = (pixels_brancos / total_pixels) * 100

    print(f"Limiar: {limiar}")
    print(f"Total de pixels: {total_pixels}")
    print(f"Pixels brancos: {pixels_brancos}")
    print(f"Porcentagem de pixels brancos: {porcentagem_brancos:.2f}%")
    print("-" * 30)

    cv2.imwrite(f"./assets/exercicio03/imagem_binaria_limiar_{limiar}_exercicio03.jpg", binaria)