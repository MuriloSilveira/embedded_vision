from django.shortcuts import render
from django.template import loader
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from django.contrib import messages
from .forms import JobForm
from .forms import CalibForm
from .forms import ResCalibForm
from .forms import QueryDayForm
from .forms import QueryLoteForm
from .models import Calibracao
from .models import Medida
from livevideo.my_functions import *
import cv2
import threading
import pickle
import numpy as np
import statistics

# Declaração Inicial de Variaveis==========================
Area = 2000
lim_min_erro = 10
calib_ok = False  # Flag calibração executada
en_cam = 0
prox_quadrante = 0
n_blocos = 0
n_blocos_atual = 0
cont = 0
erro_calib=10
res_altura=0
res_largura=0
calib_nome='Inicial'
calib=[[25,25],[25, 25],[25 ,25], [25 ,25] ,[25 ,25],[25, 25] ,[25, 25] ,[25, 25] ,[25, 25]]
job_calib=[[25,25],[25, 25],[25 ,25], [25 ,25] ,[25 ,25],[25, 25] ,[25, 25] ,[25, 25] ,[25, 25]]
job_valor_max_x = 0
job_valor_max_y = 0
job_valor_min_x = 0
job_valor_min_y = 0
job_lote = 0
job_camera = ''
dpa_x=0
dpa_y=0
media_x=0
media_y=0
mediana_x=0
mediana_y=0
moda_x=0
moda_y=0
max_x=0
max_y=0
min_x=0
min_y=0
status=[[15,'Sistema Pronto'],[10,'Aguardando Configuração'],[20,'Sistema Ativo'],[30,'Sistema Suspenso'],[50,'Sistema em Falha']]
mode=10
query_data=''
query_lote=0
#============================

# Inicio das Views

def index(request):
    global dpa_x
    global dpa_y
    global media_x
    global media_y
    global mediana_x
    global mediana_y
    global moda_x
    global moda_y
    global max_x
    global max_y
    global min_x
    global min_y
    # =========== DIV - ÚLTIMAS 5 MEDIDAS ==========================
    # Obtendo todos os dados do banco
    medidas = Medida.objects.all()
    cont = 0
    # Contando quantos tem
    for i in medidas:
        cont = cont + 1
    # Estamelecendo o limite para o query
    if cont < 6:
        salvos = medidas
    else:
        id_lim = cont - 4
        # Realizando o Query
        salvos = Medida.objects.filter(id__gte=id_lim).order_by('-data', '-horario')
    # ============ DIV - USUÁRIO ATUAL ===============================
    if str(request.user) == 'AnonymousUser':
        status_log = 'Usuário não logado'
        status_user = 'Usuário Anônimo'
    else:
        status_log = 'Usuário Logado'
        status_user = request.user
    # ============ DIV - VALORES ATUAIS DO LOTE ======================
    lote = job_lote
    valores_x=[]
    valores_y=[]
    if job_lote is not 0:
        query=Medida.objects.filter(lote=job_lote)
        for i in query:
            valores_x.append(float(i.valor_x))
            valores_y.append(float(i.valor_y))
        if len(valores_x) > 15:
            dpa_x, media_x, mediana_x, moda_x, max_x, min_x=job_statistics(valores_x)
            dpa_y, media_y, mediana_y, moda_y, max_y, min_y=job_statistics(valores_y)
    for i in range(len(status)):
        if mode is status[i][0]:
            status_lb=status[i][1]
    context = {
        'status_log': status_log,
        'status_user': status_user,
        'medidas': salvos,
        'lote': lote,
        'max_valor_x': max_x,
        'min_valor_x': min_x,
        'max_valor_y': max_y,
        'min_valor_y': min_y,
        'status': status_lb,
        'mode': mode,
        'med_valor_x': media_x,
        'med_valor_y': media_y,
        'median_valor_x': mediana_x,
        'median_valor_y': mediana_y,
        'mode_valor_x': moda_x,
        'mode_valor_y': moda_y,
        'dpa_valor_x': dpa_x,
        'dpa_valor_y': dpa_y,
    }
    return render(request, 'index.html', context)


def configuracao(request):
    global job_valor_max_x
    global job_valor_max_y
    global job_valor_min_x
    global job_valor_min_y
    global job_lote
    global job_camera
    global job_calib
    global mode
    
    form = JobForm(
        request.POST or None)
    if str(request.method) == 'POST':
        if form.is_valid():
            dados_lote = JobForm
            job_lote = form.cleaned_data.get("lote")
            job_valor_max_x = form.cleaned_data.get("max_valor_x")
            job_valor_max_y = form.cleaned_data.get("max_valor_y")
            job_valor_min_x = form.cleaned_data.get("min_valor_x")
            job_valor_min_y = form.cleaned_data.get("min_valor_y")
            job_camera = form.cleaned_data.get("camera")
            ret_calib = form.cleaned_data.get("calibracao")
            ret_calib = dict(form.fields['calibracao'].choices)[ret_calib]
            dados_calib=Calibracao.objects.filter(nome=ret_calib)
            for j in dados_calib:
                job_calib[0][0]=float(j.val_x1)
                job_calib[0][1]=float(j.val_y1)
                job_calib[1][0]=float(j.val_x2)
                job_calib[1][1]=float(j.val_y2)
                job_calib[2][0]=float(j.val_x3)
                job_calib[2][1]=float(j.val_y3)
                job_calib[3][0]=float(j.val_x4)
                job_calib[3][1]=float(j.val_y4)
                job_calib[4][0]=float(j.val_x5)
                job_calib[4][1]=float(j.val_y5)
                job_calib[5][0]=float(j.val_x6)
                job_calib[5][1]=float(j.val_y6)
                job_calib[6][0]=float(j.val_x7)
                job_calib[6][1]=float(j.val_y7)
                job_calib[7][0]=float(j.val_x8)
                job_calib[7][1]=float(j.val_y8)
                job_calib[8][0]=float(j.val_x9)
                job_calib[8][1]=float(j.val_y9)
            messages.success(request, 'Dados do Lote Salvos com Sucesso')
            mode=15
        else:
            messages.error(request, 'Erro ao salvar os dados do Lote')
    if str(request.user) == 'AnonymousUser':
        status_log = 'Usuário não logado'
        status_user = 'Usuário Anônimo'
    else:
        status_log = 'Usuário Logado'
        status_user = request.user
    context = {
        'status_log': status_log,
        'status_user': status_user,
        'form': form
    }

    return render(request, 'configuracao.html', context)


def m_calibracao(request):
    global calib_camera
    
    m_calibform = CalibForm(
        request.POST or None)
    
    if str(request.user) == 'AnonymousUser':
        status_log = 'Usuário não logado'
        status_user = 'Usuário Anônimo'
    else:
        status_log = 'Usuário Logado'
        status_user = request.user
    context = {
        'status_log': status_log,
        'status_user': status_user,
        'm_calibform': m_calibform
    }
    calib_camera = VideoCamera()
    return render(request, 'm_calibracao.html', context)


def r_calibracao(request):
    global n_blocos
    global erro_calib
    global calib_nome
    
    calib_status=erro_calib
    status_calib='Deu errado'
    m_calibform = CalibForm(
        request.POST or None)
    if str(request.method) == 'POST':
        if m_calibform.is_valid():
            calib_nome = m_calibform.cleaned_data.get("nome")
            n_blocos = int(m_calibform.cleaned_data.get("n_amost"))
        else:
            messages.error(request, 'Erro ao salvar os dados iniciais da calibração')
    if erro_calib is 1:
        status_calib='Garanta que o aruco está na posição demarcada em vermelho'
        erro_calib=0
    elif erro_calib is 2:
        status_calib='Tamanho do pixel demarcado com sucesso! Posicione no próximo quadrante'
        erro_calib=0
    elif erro_calib is 10:
        status_calib='Posicione o aruco na posição demarcada e avance para o próximo quadrante'
        erro_calib=0
    elif erro_calib is 3:
        status_calib='Calibração Concluída'
        erro_calib=0
    elif erro_calib is 4:
        status_calib='Calibração da primeira amostra concluída, inicie a próxima'
        erro_calib=0
    elif erro_calib is 5:
        status_calib='Calibração da segunda amostra concluída, inicie a próxima'
        erro_calib=0
    if str(request.user) == 'AnonymousUser':
        status_log = 'Usuário não logado'
        status_user = 'Usuário Anônimo'
    else:
        status_log = 'Usuário Logado'
        status_user = request.user
    context = {
        'status_log': status_log,
        'status_user': status_user,
        'status_calib':status_calib,
        'calib_status':calib_status
    }
    return render(request, 'r_calibracao.html', context)


def f_calibracao(request):
    global res_altura
    global res_largura
    
    form = ResCalibForm(
        request.POST or None)
    if str(request.user) == 'AnonymousUser':
        status_log = 'Usuário não logado'
        status_user = 'Usuário Anônimo'
    else:
        status_log = 'Usuário Logado'
        status_user = request.user
    context = {
        'status_log': status_log,
        'status_user': status_user,
        'form': form
    }
    return render(request, 'f_calibracao.html',context)

def result_calib(request):
    global res_altura
    global res_largura
    global calib_camera
    
    form = ResCalibForm(
        request.POST or None)
    if str(request.method) == 'POST':
        if form.is_valid():
            res_altura = float(form.cleaned_data.get("altura"))
            res_largura = float(form.cleaned_data.get("largura"))
            messages.success(request, 'Dimensões da amostra salvas com sucesso')
        else:
            messages.error(request, 'Erro ao salvar as dimensões da amostra')
    for i in range(n_blocos):
        for j in range(len(calib[0])):
            calib[i][j][0]=res_largura/calib[i][j][0]
            calib[i][j][1]=res_altura/calib[i][j][1]
    px_calib=np.empty([9,2])
    for j in range(len(calib[0])):
        px_calib[j][0]=0
        px_calib[j][1]=0
        for i in range(n_blocos):
            px_calib[j][0]=px_calib[j][0]+calib[i][j][0]
            px_calib[j][1]=px_calib[j][1]+calib[i][j][1]
        px_calib[j][0]=px_calib[j][0]/n_blocos
        px_calib[j][1]=px_calib[j][1]/n_blocos
    new_calib = Calibracao(nome=calib_nome, n_amostra=n_blocos, val_x1=px_calib[0][0], val_y1=px_calib[0][1], val_x2=px_calib[1][0], val_y2=px_calib[1][1], val_x3=px_calib[2][0], val_y3=px_calib[2][1], val_x4=px_calib[3][0], val_y4=px_calib[3][1], val_x5=px_calib[4][0], val_y5=px_calib[4][1], val_x6=px_calib[5][0], val_y6=px_calib[5][1], val_x7=px_calib[6][0], val_y7=px_calib[6][1], val_x8=px_calib[7][0], val_y8=px_calib[7][1], val_x9=px_calib[8][0], val_y9=px_calib[8][1])
    new_calib.save()
    calib_ok=True
    calib_camera.fecha()
    
    # ============ DIV - USUÁRIO ATUAL ===============================
    if str(request.user) == 'AnonymousUser':
        status_log = 'Usuário não logado'
        status_user = 'Usuário Anônimo'
    else:
        status_log = 'Usuário Logado'
        status_user = request.user
    # ============ DIV - RESULTADOS DA CALIBRAÇÃO ======================
    context = {
        'status_log': status_log,
        'status_user': status_user,
        'val_x1': px_calib[0][0],
        'val_y1': px_calib[0][1],
        'val_x2': px_calib[1][0],
        'val_y2': px_calib[1][1],
        'val_x3': px_calib[2][0],
        'val_y3': px_calib[2][1],
        'val_x4': px_calib[3][0],
        'val_y4': px_calib[3][1],
        'val_x5': px_calib[4][0],
        'val_y5': px_calib[4][1],
        'val_x6': px_calib[5][0],
        'val_y6': px_calib[5][1],
        'val_x7': px_calib[6][0],
        'val_y7': px_calib[6][1],
        'val_x8': px_calib[7][0],
        'val_y8': px_calib[7][1],
        'val_x9': px_calib[8][0],
        'val_y9': px_calib[8][1]
    }
    return render(request, 'result_calib.html', context)

def result_q_dia(request):
    form = QueryDayForm(
        request.POST or None)
    
    if str(request.user) == 'AnonymousUser':
        status_log = 'Usuário não logado'
        status_user = 'Usuário Anônimo'
    else:
        status_log = 'Usuário Logado'
        status_user = request.user
    context = {
        'status_log': status_log,
        'status_user': status_user,
        'form': form
    }
    return render(request, 'result_q_dia.html',context)

def result_q_lote(request):
    global query_data
    form = QueryDayForm(
        request.POST or None)
    if str(request.method) == 'POST':
        if form.is_valid():
            ret_dia=form.cleaned_data.get("dia")
            ret_dia = dict(form.fields['dia'].choices)[ret_dia]
            query_data=ret_dia
        else:
            messages.error(request, 'Erro ao salvar os dados do Lote')
    form = QueryLoteForm(
        request.POST or None)
    
    if str(request.user) == 'AnonymousUser':
        status_log = 'Usuário não logado'
        status_user = 'Usuário Anônimo'
    else:
        status_log = 'Usuário Logado'
        status_user = request.user
    context = {
        'status_log': status_log,
        'status_user': status_user,
        'form': form
    }
    return render(request, 'result_q_lote.html', context)

def result_query(request):
    global query_lote
    
    form = QueryLoteForm(
        request.POST or None)
    if str(request.method) == 'POST':
        if form.is_valid():
            ret_lote=form.cleaned_data.get("lote")
            ret_lote = dict(form.fields['lote'].choices)[ret_lote]
            query_lote=ret_lote
        else:
            messages.error(request, 'Erro ao salvar o filtro de Lote')
    query=Medida.objects.filter(data=query_data, lote=query_lote)
    
    if str(request.user) == 'AnonymousUser':
        status_log = 'Usuário não logado'
        status_user = 'Usuário Anônimo'
    else:
        status_log = 'Usuário Logado'
        status_user = request.user
    context = {
        'status_log': status_log,
        'status_user': status_user,
        'medidas': query,
    }
    
    return render(request, 'result_query.html',context)


class VideoCamera(object):
    def __init__(self):
        global job_camera
        self.status = False
        self.video = cv2.VideoCapture(0)
        (self.status, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def fecha(self):
        self.video.release()

    def get_frame(self):
        img = self.frame
        _, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()

    def measure_byInputs(self):
        img = self.frame
        calib=job_calib
        # Encontra os contornos do objeto alvo
        objects_contours, img, status = object_detection(img, kernel=(3, 3), minArea=2000)
        if status is not 10:
            # Desenha as linhas do retangulo presente na imagem
            img, box = squared_contour(img, objects_contours[0], center_color=(0, 0, 255),
                                       square_color=(255, 0, 0))
            # Obtem as medidas por quadrante
            distX_px = measure_norm(img, box, 0, 1, False)
            distY_px = measure_norm(img, box, 0, 3, False)

            # Tranforma em cm através do vetor de calibração
            distX = pixel2mm(distX_px, calib, tipo=0)
            distY = pixel2mm(distY_px, calib, tipo=1)

            # Verifica se existem circulos
            circle_ref, circle = detect_circles(img)
            if circle_ref is not None:
                circles_dist = np.zeros(len(circle_ref), dtype=float)
                for i in range(len(circle_ref)):
                    print("=========== OUTRO CIRCULO===============")
                    distY_px = measure_norm(img, circle_ref[i], 0, 1, True)
                    distY = pixel2mm(distY_px, calib, tipo=1)
                    circles_dist[i] = distY
            else:
                print("Nenhum circulo encontrado\n")
            # Reeordena os pontos do retagulo para uma ordem da esquerda para a direita, de cima para baixo
            new_box = order_points(box)
            # Transforma vetor para inteiro para utilizar nas funções de desenho
            new_box_int = np.int0(new_box)

            # Desenha a Arrow no Eixo X ==================
            img = drawArrow(img, new_box_int, ponto_inicial=0, ponto_final=1, Acomp=-15, X_Y=0)
            # Desenha o texto no Exio X ==================
            img = drawText(img, new_box_int, distX, ponto_inicial=0, ponto_final=1, Tcomp=-5, Acomp=-15,
                           X_Y=0)

            # Desenha a Arrow no Eixo Y ==================
            img = drawArrow(img, new_box_int, ponto_inicial=0, ponto_final=3, Acomp=-15, X_Y=1)
            # Desenha o texto no Exio Y ==================
            img = drawText(img, new_box_int, distY, ponto_inicial=0, ponto_final=3, Tcomp=-10, Acomp=-15,
                           X_Y=1)
            new_med = Medida(lote=job_lote, valor_x=distX, valor_y=distY)
            new_med.save()
        else:
            print("Erro ao encontrar contornos no objeto\n")
        _, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()

    def calibration(self):
        global prox_quadrante
        global n_blocos_atual
        global cont
        global calib
        global erro_calib

        img = self.frame
        # Definindo os limites dos quadrantes em X
        x1 = int(img.shape[1] / 3)
        x2 = int((2 * img.shape[1]) / 3)
        x3 = img.shape[1]

        # Definindo os limites dos quadrantes em Y
        y1 = int(img.shape[0] / 3)
        y2 = int((2 * img.shape[0]) / 3)
        y3 = img.shape[0]

        if cont is 0:
            # Declaro o vetor de saida das medidas encontradas em cada quadrante
            calib = np.empty([n_blocos, 9, 2])
            # Faz o loop nos 9 quadrantes
            base = img.copy()
            # Desenha os 9 quadrantes
            cv2.line(base, (x1, 0), (x1, y3), (0, 255, 0), 2)
            cv2.line(base, (x2, 0), (x2, y3), (0, 255, 0), 2)
            cv2.line(base, (0, y1), (x3, y1), (0, 255, 0), 2)
            cv2.line(base, (0, y2), (x3, y2), (0, 255, 0), 2)
            # Destaca o Quadrante 1
            cv2.line(base, (0, y1), (x1, y1), (0, 0, 255), 2)
            cv2.line(base, (x1, 0), (x1, y1), (0, 0, 255), 2)
            if prox_quadrante is 1:  # Enter
                # Obtem as medidas do aruco
                prox_quadrante = 0
                ROI = img[0:y1, 0:x1]
                calib = aruco_measure(ROI, cont, n_blocos_atual, calib, Area)
                if calib[n_blocos_atual][cont][0] < lim_min_erro or calib[n_blocos_atual][cont][
                    1] < lim_min_erro:
                    print("Insira o aruco dentro da posição demarcada em vermelho")
                    erro_calib=1
                else:
                    erro_calib=2
                    cont = cont + 1
        elif cont == 1:
            base = img.copy()
            # Desenha os 9 quadrantes
            cv2.line(base, (x1, 0), (x1, y3), (0, 255, 0), 2)
            cv2.line(base, (x2, 0), (x2, y3), (0, 255, 0), 2)
            cv2.line(base, (0, y1), (x3, y1), (0, 255, 0), 2)
            cv2.line(base, (0, y2), (x3, y2), (0, 255, 0), 2)
            # Destaca o Quadrante 2
            cv2.line(base, (x1, 0), (x1, y1), (0, 0, 255), 2)
            cv2.line(base, (x1, y1), (x2, y1), (0, 0, 255), 2)
            cv2.line(base, (x2, 0), (x2, y1), (0, 0, 255), 2)
            # Apresenta ao usuario a referencia de posicionamento
            if prox_quadrante is 1:  # Enter
                # Obtem as medidas do aruco
                prox_quadrante = 0
                ROI = img[0:y1, x1:x2]
                calib = aruco_measure(ROI, cont, n_blocos_atual, calib, Area)
                if calib[n_blocos_atual][cont][0] < lim_min_erro or calib[n_blocos_atual][cont][
                    1] < lim_min_erro:
                    print("Insira o aruco dentro da posição demarcada em vermelho")
                    erro_calib=1
                else:
                    erro_calib=2
                    cont = cont + 1
        elif cont == 2:
            base = img.copy()
            # Desenha os 9 quadrantes
            cv2.line(base, (x1, 0), (x1, y3), (0, 255, 0), 2)
            cv2.line(base, (x2, 0), (x2, y3), (0, 255, 0), 2)
            cv2.line(base, (0, y1), (x3, y1), (0, 255, 0), 2)
            cv2.line(base, (0, y2), (x3, y2), (0, 255, 0), 2)
            cv2.line(base, (x2, 0), (x2, y1), (0, 0, 255), 2)
            cv2.line(base, (x2, y1), (x3, y1), (0, 0, 255), 2)
            # Apresenta ao usuario a referencia de posicionamento
            if prox_quadrante is 1:  # Enter
                # Obtem as medidas do aruco
                prox_quadrante = 0
                ROI = img[0:y1, x2:x3]
                calib = aruco_measure(ROI, cont, n_blocos_atual, calib, Area)
                if calib[n_blocos_atual][cont][0] < lim_min_erro or calib[n_blocos_atual][cont][
                    1] < lim_min_erro:
                    print("Insira o aruco dentro da posição demarcada em vermelho")
                    erro_calib=1
                else:
                    erro_calib=2
                    cont = cont + 1
        elif cont == 3:
            base = img.copy()
            # Desenha os 9 quadrantes
            cv2.line(base, (x1, 0), (x1, y3), (0, 255, 0), 2)
            cv2.line(base, (x2, 0), (x2, y3), (0, 255, 0), 2)
            cv2.line(base, (0, y1), (x3, y1), (0, 255, 0), 2)
            cv2.line(base, (0, y2), (x3, y2), (0, 255, 0), 2)
            cv2.line(base, (0, y1), (x1, y1), (0, 0, 255), 2)
            cv2.line(base, (x1, y1), (x1, y2), (0, 0, 255), 2)
            cv2.line(base, (0, y2), (x1, y2), (0, 0, 255), 2)
            # Apresenta ao usuario a referencia de posicionamento
            if prox_quadrante is 1:  # Enter
                # Obtem as medidas do aruco
                prox_quadrante = 0
                ROI = img[y1:y2, 0:x1]
                calib = aruco_measure(ROI, cont, n_blocos_atual, calib, Area)
                if calib[n_blocos_atual][cont][0] < lim_min_erro or calib[n_blocos_atual][cont][
                    1] < lim_min_erro:
                    erro_calib=1
                    print("Insira o aruco dentro da posição demarcada em vermelho")
                else:
                    erro_calib=2
                    cont = cont + 1
        elif cont == 4:
            base = img.copy()
            # Desenha os 9 quadrantes
            cv2.line(base, (x1, 0), (x1, y3), (0, 255, 0), 2)
            cv2.line(base, (x2, 0), (x2, y3), (0, 255, 0), 2)
            cv2.line(base, (0, y1), (x3, y1), (0, 255, 0), 2)
            cv2.line(base, (0, y2), (x3, y2), (0, 255, 0), 2)
            cv2.line(base, (x1, y1), (x2, y1), (0, 0, 255), 2)
            cv2.line(base, (x2, y1), (x2, y2), (0, 0, 255), 2)
            cv2.line(base, (x1, y2), (x2, y2), (0, 0, 255), 2)
            cv2.line(base, (x1, y1), (x1, y2), (0, 0, 255), 2)
            # Apresenta ao usuario a referencia de posicionamento
            if prox_quadrante is 1:  # Enter
                # Obtem as medidas do aruco
                prox_quadrante = 0
                ROI = img[y1:y2, x1:x2]
                calib = aruco_measure(ROI, cont, n_blocos_atual, calib, Area)
                if calib[n_blocos_atual][cont][0] < lim_min_erro or calib[n_blocos_atual][cont][
                    1] < lim_min_erro:
                    erro_calib=1
                    print("Insira o aruco dentro da posição demarcada em vermelho")
                else:
                    erro_calib=2
                    cont = cont + 1
        elif cont == 5:
            base = img.copy()
            # Desenha os 9 quadrantes
            cv2.line(base, (x1, 0), (x1, y3), (0, 255, 0), 2)
            cv2.line(base, (x2, 0), (x2, y3), (0, 255, 0), 2)
            cv2.line(base, (0, y1), (x3, y1), (0, 255, 0), 2)
            cv2.line(base, (0, y2), (x3, y2), (0, 255, 0), 2)
            cv2.line(base, (x2, y1), (x3, y1), (0, 0, 255), 2)
            cv2.line(base, (x2, y1), (x2, y2), (0, 0, 255), 2)
            cv2.line(base, (x2, y2), (x3, y2), (0, 0, 255), 2)
            # Apresenta ao usuario a referencia de posicionamento
            if prox_quadrante is 1:  # Enter
                # Obtem as medidas do aruco
                prox_quadrante = 0
                ROI = img[y1:y2, x2:x3]
                calib = aruco_measure(ROI, cont, n_blocos_atual, calib, Area)
                if calib[n_blocos_atual][cont][0] < lim_min_erro or calib[n_blocos_atual][cont][
                    1] < lim_min_erro:
                    erro_calib=1
                    print("Insira o aruco dentro da posição demarcada em vermelho")
                else:
                    erro_calib=2
                    cont = cont + 1
        elif cont == 6:
            base = img.copy()
            # Desenha os 9 quadrantes
            cv2.line(base, (x1, 0), (x1, y3), (0, 255, 0), 2)
            cv2.line(base, (x2, 0), (x2, y3), (0, 255, 0), 2)
            cv2.line(base, (0, y1), (x3, y1), (0, 255, 0), 2)
            cv2.line(base, (0, y2), (x3, y2), (0, 255, 0), 2)
            cv2.line(base, (0, y2), (x1, y2), (0, 0, 255), 2)
            cv2.line(base, (x1, y2), (x1, y3), (0, 0, 255), 2)
            # Apresenta ao usuario a referencia de posicionamento
            if prox_quadrante is 1:  # Enter
                # Obtem as medidas do aruco
                prox_quadrante = 0
                ROI = img[y2:y3, 0:x1]
                calib = aruco_measure(ROI, cont, n_blocos_atual, calib, Area)
                if calib[n_blocos_atual][cont][0] < lim_min_erro or calib[n_blocos_atual][cont][
                    1] < lim_min_erro:
                    erro_calib=1
                    print("Insira o aruco dentro da posição demarcada em vermelho")
                else:
                    erro_calib=2
                    cont = cont + 1
        elif cont == 7:
            base = img.copy()
            # Desenha os 9 quadrantes
            cv2.line(base, (x1, 0), (x1, y3), (0, 255, 0), 2)
            cv2.line(base, (x2, 0), (x2, y3), (0, 255, 0), 2)
            cv2.line(base, (0, y1), (x3, y1), (0, 255, 0), 2)
            cv2.line(base, (0, y2), (x3, y2), (0, 255, 0), 2)
            cv2.line(base, (x1, y2), (x2, y2), (0, 0, 255), 2)
            cv2.line(base, (x1, y2), (x1, y3), (0, 0, 255), 2)
            cv2.line(base, (x2, y2), (x2, y3), (0, 0, 255), 2)
            # Apresenta ao usuario a referencia de posicionamento
            if prox_quadrante is 1:  # Enter
                # Obtem as medidas do aruco
                prox_quadrante = 0
                ROI = img[y2:y3, x1:x2]
                calib = aruco_measure(ROI, cont, n_blocos_atual, calib, Area)
                if calib[n_blocos_atual][cont][0] < lim_min_erro or calib[n_blocos_atual][cont][
                    1] < lim_min_erro:
                    erro_calib=1
                    print("Insira o aruco dentro da posição demarcada em vermelho")
                else:
                    erro_calib=2
                    cont = cont + 1
        else:
            base = img.copy()
            # Desenha os 9 quadrantes
            cv2.line(base, (x1, 0), (x1, y3), (0, 255, 0), 2)
            cv2.line(base, (x2, 0), (x2, y3), (0, 255, 0), 2)
            cv2.line(base, (0, y1), (x3, y1), (0, 255, 0), 2)
            cv2.line(base, (0, y2), (x3, y2), (0, 255, 0), 2)
            cv2.line(base, (x2, y2), (x3, y2), (0, 0, 255), 2)
            cv2.line(base, (x2, y2), (x2, y3), (0, 0, 255), 2)
            # Apresenta ao usuario a referencia de posicionamento
            if prox_quadrante is 1:  # Enter
                # Obtem as medidas do aruco
                prox_quadrante = 0
                ROI = img[y2:y3, x2:x3]
                calib = aruco_measure(ROI, cont, n_blocos_atual, calib, Area)
                if calib[n_blocos_atual][cont][0] < lim_min_erro or calib[n_blocos_atual][cont][
                    1] < lim_min_erro:
                    erro_calib=1
                    print("Insira o aruco dentro da posição demarcada em vermelho")
                else:
                    cont = 0
                    n_blocos_atual = n_blocos_atual + 1
                    if n_blocos_atual == n_blocos:
                        erro_calib=3
                    elif n_blocos_atual == 1:
                        erro_calib=4
                    elif n_blocos_atual == 2:
                        erro_calib=5
                    
        _, jpeg = cv2.imencode('.jpg', base)
        return jpeg.tobytes()
    
    #def getCalib(self):
        

    def off(self):
        img = cv2.imread('/home/pi/SMI/django00/livevideo/static/images/video_off.png')
        _, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.status, self.frame) = self.video.read()


def generate_frame():
    global en_cam
    if en_cam is 0:
        img = cv2.imread('/home/pi/SMI/django00/livevideo/static/images/video_off.png')
        _, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
    while True:
        if en_cam is 1:
            frame = camera.measure_byInputs()
        yield (b'--frame\r\n'
               b'Content-Type: imagem/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def calib_generate_frame():
    while True:
        frame = calib_camera.calibration()
        yield (b'--frame\r\n'
               b'Content-Type: imagem/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video(request):
    return StreamingHttpResponse(generate_frame(), content_type="multipart/x-mixed-replace;boundary=frame")


def calib_video(request):
    return StreamingHttpResponse(calib_generate_frame(), content_type="multipart/x-mixed-replace;boundary=frame")


def prox_calib(request):
    global prox_quadrante
    prox_quadrante = 1
    return HttpResponse("""<html><script>window.location.replace('/calib');</script></html>""")

def liga(request):
    global en_cam
    global camera
    global mode
    
    if mode is not 10:
        camera = VideoCamera()
        en_cam = 1
        mode=20
    else:
        print("falta configuracao\n")
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")


def desliga(request):
    global en_cam
    global camera
    global mode
    
    if mode is 20 or mode is 50:
        camera.fecha()
        del camera
        en_cam = 0
        mode=30
    else:
        print("Nao pode desligar, mode is not 20 or 50")
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")
