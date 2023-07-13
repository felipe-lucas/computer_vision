# Importar as bibliotecas (openCV e numpy)
import cv2 as cv
import numpy as np
# Abrir e criar conexão com a câmera [parâmetro 0 significa a câmera principal]
# O parâmetro cv.CAP_DSHOW para ajudar na detecção da câmera
video = cv.VideoCapture(0, cv.CAP_DSHOW)
# Verificar se a câmera abriu
if not video.isOpened():
  print("Aguardando abrir câmera")
# Definir as coordenadas dos círculos que especificam a peça OK (coordenadas ajustadas
manualmente ao abrir a câmera)
circle_1 = [333, 265]
circle_2 = [332, 413]
# Especificar o raio do círculo de modo a abranger o perímetro dos dois furos
radius = 35
# Variáveis para exibição dos resultados
result = ''
color = [0, 0, 0]
# Loop para leitura e análise das imagens da webcam
while True:
  # Ler a imagem da câmera
  check, img = video.read()
  # Identificar se existe algum problema com a câmera
  if not check:
    print("Nenhum frame detectado")
    break
  # Obter as dimensões da imagem capturada pela câmera
  width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
  height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
  # Criar máscara preta com as dimensões obtidas anteriormente
  mask = np.zeros((height, width), dtype = np.uint8)
  # Desenhar um círculo branco na máscara criada
  cv.circle(mask, circle_1, radius, (255, 255, 255), -1)
  cv.circle(mask, circle_2, radius, (255, 255, 255), -1)
  # Transformar a imagem em escalas de cinza
  gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
  # Aplicar um filtro para fazer a limiarização da imagem
  ret, thresh = cv.threshold(gray, 70, 255, cv.THRESH_BINARY_INV)
  # Furo superior
  # Aplicação de uma lógica para interseção dos bits da limiarização com a máscara preta
  intersec_1 = cv.bitwise_and(thresh, thresh, mask=mask)
  # Contar os pixels brancos na região de interesse do primeiro furo
  Wpixels_01 = cv.countNonZero(intersec_1)
  # Furo inferior
  # Aplicação de uma lógica para interseção dos bits da limiarização com a máscara preta
  intersec_2 = cv.bitwise_and(thresh, thresh, mask=mask)
  # Contar os pixels brancos na região de interesse do segundo furo
  Wpixels_02 = cv.countNonZero(intersec_2)
  # Exibir na tela o número de pixels detectados em cada região
  # Furo superior
  cv.putText(img,str(Wpixels_01), (circle_1[0]+50, circle_1[1]+5),
  cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
  # Furo inferior
  cv.putText(img,str(Wpixels_02), (circle_2[0]+50, circle_2[1]+5),
  cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
  # Desenhar um círculo na imagem original na cor vermelha para conferência do
  posicionamento da região do furo
  # Furo superior
  cv.circle(img, circle_1, radius, (0,0,255), 2)
  # Furo inferior
  cv.circle(img, circle_2, radius, (0,0,255), 2)
  # Criação da lógica para identificação das peças OK e NOK
  if ((Wpixels_01+Wpixels_02)/2) <10:
    # Mudança da variável result para OK
    result = 'OK'
    # Mudança da variável color para a cor verde
    color = [0, 255, 0]
  else:
    # Mudança da variável result para NOK
    result = 'NOK'
    # Mudança da variável color para a cor vermelha
    color = [0, 0, 255]
  # Inserir no vídeo o resultado da análise da peça (OK/NOK)
  cv.putText(img, result, (20,40), cv.FONT_HERSHEY_SIMPLEX, 1, (color[0],
  color[1], color[2]), 2)
  # Exibir uma tela com a imagem juntamente com as informações obtidas da peça
  cv.imshow("video", img)
  # Exibir uma tela com o vídeo com filtro de limiarização
  cv.imshow("video THRESH", thresh)
  # Aguardar um tempo para pressionar uma tecla
  KEY = cv.waitKey(1)
  # Condição: Se a tecla "q" for pressionada a janela é fechada
  if KEY == ord('q'):
    break
# Liberar objeto de captura de vídeo
video.release()
# Fechar todas as janelas abertas
cv.destroyAllWindows()
