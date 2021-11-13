import cv2
import numpy as np
import math
import pickle
import statistics

def teste(img):
    gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#Converter a imagem para a escala de cinza
    blured_img=cv2.GaussianBlur(gray_img,(5,5),0)
    imgCanny = cv2.Canny(blured_img, 100, 255)
    contours, hierar= cv2.findContours(imgCanny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  # cv2.RETR_TREE - para encontrar os contornos externos
    return imgCanny

def object_detection(img,kernel=(5,5),minArea=2000):
    #Aplica uma mascara para encontrar o objeto
    gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#Converter a imagem para a escala de cinza
    #cv2.imshow("gray_img",gray_img)
    blured_img=cv2.GaussianBlur(gray_img,kernel,0)#Aplica um filtro contra ruido de frequencia da rede
    #cv2.imshow("blured_img",blured_img)
    imgCanny = cv2.Canny(blured_img, 100, 255)  # obtem os contornos da imagem de acordo com a variação da escala de cinza, definas nos limitantes
    #cv2.imshow("canny",imgCanny)
    #Encontra os contornos da imagem
    contours, hierar= cv2.findContours(imgCanny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  # cv2.RETR_TREE - para encontrar os contornos externos
    #print("contours\n",contours)
    objects_contours = []#Defini um vetor para armazenar os contornos do objeto
    #Varre o vetor de contorno e inclui apenas os dos objetos com área conforme necessário
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #print("Area ",area)
        if area > minArea:
            objects_contours.append(cnt)
    status=0
    if len(objects_contours)==0:#Verifica se não foram encontrado pontos de contorno para o objeto
        status=10
    return objects_contours, img,status

def job_statistics(lista):
    media=statistics.mean(lista)
    mediana=statistics.median(lista)
    moda=statistics.mode(lista)
    maior= max(lista)
    menor=min(lista)
    soma=0
    for i in lista:
        soma=soma+(i-media)**2
    n=len(lista)
    total=soma/(n-1)
    dpa=total**(1/2)
    
    return dpa, media, mediana, moda, maior, menor

def squared_contour(img,cnt,center_color=(0,0,255),square_color=(255,0,0)):
    #Obtem o retangulo em volta do objeto - x, y - pontos cartesianos do centro do objeto, tamanho do retangulo, rotação em sentido horario
    rect=cv2.minAreaRect(cnt)
    (x,y),_,_=rect
    cv2.circle(img,(int(x),int(y)),5,center_color,-1)#Desenha um circulo vermelho no centro do retangulo encontrado
    box=cv2.boxPoints(rect)#Defini os pontos cartesianos do retangulo
    box_int=np.int0(box)#Transforma os valores para inteiro, para nao dar erro na funcao de desenho
    #Desenha as linhas do retangulo presente na imagem
    cv2.polylines(img,[box_int],True,square_color,2)
    
    return img,box

def order_points(box):
    #Reordenando os pontos do retangulo======================
    new_box=np.zeros_like(box)#Cria vetor com novos pontos
    add=box.sum(axis=-1)#Soma o eixo x com o y
    # O maior será o ponto 2 e o menor o ponto 0
    new_box[2]=box[np.argmax(add)]
    new_box[0]=box[np.argmin(add)]
    #o menor será o ponto 1 e o maior o pont 3
    diff=np.diff(box,axis=-1)#Faz a diferença entre o y e o x,
    new_box[1]=box[np.argmin(diff)]
    new_box[3]=box[np.argmax(diff)]
    
    return new_box

def drawArrow(img,box,ponto_inicial,ponto_final,Acomp,X_Y=0,color=(0,255,0),thickness=2):
    #Calculando os catetos
    if X_Y==0:#0 - desenho de uma arrow em X ===== 1- em Y
        cateto_oposto=box[ponto_inicial][1]-box[ponto_final][1]
        cateto_adj=box[ponto_final][0]-box[ponto_inicial][0]
    else:
        cateto_adj=box[ponto_final][1]-box[ponto_inicial][1]
        cateto_oposto=box[ponto_final][0]-box[ponto_inicial][0]  
    #Desenhando arrow
    angle=math.degrees(math.atan(cateto_oposto/cateto_adj))#Angulo da posição da arrow em relaçao ao ponto inicial
    if X_Y==0: #0 - desenho de uma arrow em X ===== 1- em Y
        #Compensação em Y e X para o posicionamento da arrow
        Acomp_x=int(Acomp*math.tan(math.radians(angle)))
    else:# 1- em Y
        Acomp_x=Acomp
        Acomp=int(-Acomp_x*math.tan(math.radians(angle)))   
    #Desenhando arrow
    cv2.arrowedLine(img,(box[ponto_inicial][0]+Acomp_x,box[ponto_inicial][1]+Acomp),(box[ponto_final][0]+Acomp_x,box[ponto_final][1]+Acomp),color,thickness,4)
    
    return img
    
def drawText(img,box,dist,ponto_inicial,ponto_final,Tcomp,Acomp,X_Y=0,color=(0,255,0),thickness=2):    
    h_img = img.shape[0]
    w_img = img.shape[1]
    
    #Calculando os catetos
    if X_Y==0:#0 - desenho de uma arrow em X ===== 1- em Y
        cateto_oposto=box[ponto_inicial][1]-box[ponto_final][1]
        cateto_adj=box[ponto_final][0]-box[ponto_inicial][0]
    else:
        cateto_adj=box[ponto_final][1]-box[ponto_inicial][1]
        cateto_oposto=box[ponto_final][0]-box[ponto_inicial][0]  
    #Desenhando arrow
    angle=math.degrees(math.atan(cateto_oposto/cateto_adj))#Angulo da posição da arrow em relaçao ao ponto inicial
    
    if X_Y==0: #0 - desenho de um texto em X ===== 1- em Y
        #Compensação em Y e X para o posicionamento do texto
        Tcomp_x=int(Tcomp*math.tan(math.radians(angle)))
        #Compensação em Y e X para o posicionamento da arrow
        Acomp_x=int(Acomp*math.tan(math.radians(angle)))
        #Define as posições do texto indicativo da medida, sendo que compensa duas vez - uma pela arrow e outra pelo texto
        pos_text_w_x=int(box[ponto_inicial][0]+ Acomp_x + Tcomp_x)
        pos_text_w_y=int(box[ponto_inicial][1]+ Acomp + Tcomp)
    else:
        Tcomp_x=Tcomp
        Tcomp=int(-Tcomp_x*math.tan(math.radians(angle)))
        Acomp_x=Acomp
        Acomp=int(-Acomp_x*math.tan(math.radians(angle)))
        pos_text_w_x=int(box[ponto_inicial][0]+Acomp_x+3*Tcomp_x)
        pos_text_w_y=int(box[ponto_inicial][1]+Acomp+3*Tcomp)
    
    
    #Transforma o valor do eixo Y e transforma em string
    valor_format="{:.2f}".format(dist) +" mm"
    #valor_format=map('{:.2f}%'.format,dist) +' cm'
    
    #Artificio para Rotacionar o texto no Angulo que está o objeto
    img_text=np.zeros((h_img,w_img),dtype=np.uint8)#Cria uma imagem de mesmo tamanho e cor preto para rotacionar o texto
    if X_Y==0: #0 - desenho de um texto em X ===== 1- em Y
        angle_text=angle #Angulo do texto
    else:
        angle_text=angle -90#Angulo do texto - sempre em -90° pois a posição angular inicial é defasada em 90° - (eixo Y)
    cv2.putText(img_text,valor_format,(pos_text_w_x,pos_text_w_y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1,cv2.LINE_AA)#Coloca o texto do eixo Y nessa imagem
    M=cv2.getRotationMatrix2D((pos_text_w_x,pos_text_w_y),angle_text,1)#Cria uma matriz de rotação
    out=cv2.warpAffine(img_text,M,(img_text.shape[1],img.shape[0]))#Imagem rotacionada
    _,mask_rot_text=cv2.threshold(out,0,255,cv2.THRESH_BINARY_INV)#Cria uma mascara para binarizar a imagem com o texto
    img=cv2.bitwise_and(img,img,mask=mask_rot_text)#Utiliza a operação AND para unir a imagem original com a imagem do texto
    
    return img

def aruco_measure(img,cont,n_bloco,calib,minArea):
    #Obtem valores
    objects_contours,img,status=object_detection(img,(5,5),10000)
    for cnt in objects_contours:
        area = cv2.contourArea(cnt)  # Calcula a area do contorno
        if area > minArea:
            #Obtem o retangulo em volta do objeto - x, y - pontos cartesianos do centro do objeto, tamanho do retangulo, rotação em sentido horario
            rect=cv2.minAreaRect(cnt)
            box=cv2.boxPoints(rect)#Defini os pontos cartesianos do retangulo
            #Reeordena os pontos do retagulo para uma ordem da esquerda para a direita, de cima para baixo
            new_box=order_points(box)
            
            #Calcula o comprimento das arestas===================
            #Aresta - Ponto 0 e 1
            cateto_oposto_x=new_box[0][1]-new_box[1][1]
            cateto_adj_x=new_box[1][0]-new_box[0][0]
            distX=(cateto_adj_x**2 + cateto_oposto_x**2)**0.5
            #Aresta - Ponto 0 e 3
            cateto_adj_y=new_box[3][1]-new_box[0][1]
            cateto_oposto_y=new_box[3][0]-new_box[0][0]
            distY=(cateto_adj_y**2 + cateto_oposto_y**2)**0.5
            #Salva no array de calibração
            print("distX é %f e distY é %4.2f" % (distX,distY))
            calib[n_bloco][cont][0]=distX
            calib[n_bloco][cont][1]=distY
        else:
            print("Area Muito pequena")
        
    return calib

def measure_norm(img,box,inicial=0,final=1,circle=False):
    #Definindo os limites dos quadrantes em X
    x1=int(img.shape[1]/3)
    x2=int((2*img.shape[1])/3)
    x3=img.shape[1]
    #Definindo os limites dos quadrantes em Y
    y1=int(img.shape[0]/3)
    y2=int((2*img.shape[0])/3)
    y3=img.shape[0]
    if circle is False:
        #Reeordena os pontos do retagulo para uma ordem da esquerda para a direita, de cima para baixo
        new_box=order_points(box)
        #===== Aresta - Ponto 0 a 1
        #Calculo da Equação da Reta
        px1=int(new_box[inicial][0])
        py1=int(new_box[inicial][1])
        px2=int(new_box[final][0])
        py2=int(new_box[final][1])
    else:
        #Passando as coordenadas das semireta formadas pelo circulo
        px1=box[0][0]
        py1=box[0][1]
        px2=box[1][0]
        py2=box[1][1]
    if px1==px2:
        a_n_existe=True
        print("Não existe coeficiente angular no segmento de reta - %d e %d" % (inicial,final))
        #Analisa as 6 condicoes possiveis de posicionamento do pontos inicial e final do eixo X
        if (py1<y1 and py2<=y1) or (py1>=y1 and py1<y2 and py2>y1 and py2<=y2) or (py1>=y2 and py2>y2):#Caso 1,2,3 
            p_reta01=np.zeros([2,3],dtype=int)#Defini o vetor com os pontos do segmento de reta
            p_reta01[0][0]=px1
            p_reta01[0][1]=py1
            p_reta01[1][0]=px2
            p_reta01[1][1]=py2
            print("Caso 1,2,3 - py1 -> %d    py2 -> %d", (py1,py2))
            cont=0#Contador de quantos pontos foram encontrados cruzando os eixos Y limites (y1 e y2)
        elif py1<y1 and py2>y1 and py2<=y2:#Caso 4
            p_reta01=np.zeros([3,3],dtype=int)#Defini o vetor com os pontos do segmento de reta
            p_reta01[0][0]=px1
            p_reta01[0][1]=py1
            p_reta01[1][0]=px1
            p_reta01[1][1]=y1
            p_reta01[2][0]=px2
            p_reta01[2][1]=py2
            cont=1#Contador de quantos pontos foram encontrados cruzando os eixos Y limites (y1 e y2)
        elif py1>=y1 and py1<y2 and py2>y2:#Caso 5
            p_reta01=np.zeros([3,3],dtype=int)#Defini o vetor com os pontos do segmento de reta
            p_reta01[0][0]=px1
            p_reta01[0][1]=py1
            p_reta01[1][0]=px1
            p_reta01[1][1]=y2
            p_reta01[2][0]=px2
            p_reta01[2][1]=py2
            cont=1#Contador de quantos pontos foram encontrados cruzando os eixos Y limites (y1 e y2)
        elif py1<y1 and py2>y2:#Caso 6
            p_reta01=np.zeros([4,3],dtype=int)#Defini o vetor com os pontos do segmento de reta
            p_reta01[0][0]=px1
            p_reta01[0][1]=py1
            p_reta01[1][0]=px1
            p_reta01[1][1]=y1
            p_reta01[2][0]=px2
            p_reta01[2][1]=y2
            p_reta01[3][0]=px2
            p_reta01[3][1]=py2
            cont=2#Contador de quantos pontos foram encontrados cruzando os eixos Y limites (y1 e y2)
        else:
            print("----- Erro na formação dos pontos da reta para 'a' não existente------")
            print("----- Ponto Inicial (%d,%d) -- Ponto Final (%d,%d) ------"%(px1,py1,px2,py2))
            print("----- Limites: x1=%d x2=%d x3=%d (tamanho total x) y1=%d y2=%d y3=%d (tamanho total y) ------"%(x1,x2,x3,y1,y2,y3))
    else:
        a=(py2-py1)/(px2-px1)
        b=(-a*px1)+py1
        if py1==int(a*px1+b):
            print("\nSegmento de reta - %d e %d - Validação da Equação da Reta - Ponto %d OK\n" % (inicial,final,inicial))
        else:
            print("Erro equação - y1....e calculo %d",(py1,int(a*px1+b)))
        if py2==int(a*px2+b):
            print("\nSegmento de reta - %d e %d - Validação da Equação da Reta - Ponto %d OK\n" % (inicial,final,final))
        else:
            print("Erro equação - y2.... %d e calculo %d" % (py2,int(a*px2+b)))
        #Analisar quais pontos dos principais eixos a equação da reta satisfaz
        #Equação da Reta entre ponto 0 e 1
        p_reta01=np.zeros([6,3],dtype=int)#6 pois é o maximo de pontos possiveis para a matriz 3x3 de calibração
        #Defini os pontos iniciais e finais da reta
        p_reta01[0][0]=px1
        p_reta01[0][1]=py1
        p_reta01[1][0]=px2
        p_reta01[1][1]=py2
        #Busca por mais pontos de referencia=========
        cont=0#Contador de quantos pontos foram encontrados
        #Variando o Eixo Y
        for i in range(2):
            if i==0: #- Para X1 (img.shape[1]/3)
                x_var=x1
            else: #- Para X2 (2*img.shape[1]/3)
                x_var=x2
            if px1<=x_var and px2>=x_var:#Analisar se o eixo fixado cruza a reta em analise
                for j in range(y3):
                    calculo=int((a*x_var)+b)
                    if j==calculo:#Verificando se o ponto passa pela reta
                        #Passa o par ordenado que passa a reta
                        p_reta01[2+cont][0]=x_var
                        p_reta01[2+cont][1]=j
                        cont=cont+1
            print("Variando eixo X - p_reta01\n",p_reta01)
        #Variando o Eixo X
        for i in range(2):
            if i==0: #- Para Y1 (img.shape[0]/3)
                y_var=y1
            else:#- Para y2 (2*img.shape[0]/3)
                y_var=y2
            if (py1<y_var and py2>y_var) or (py1>y_var and py2<y_var):#Analisar se o eixo fixado cruza a reta em analise
                for j in range(x3):
                    calculo=int((y_var-b)/a)
                    if j==calculo:#Verificando se o ponto passa pela reta
                        p_reta01[2+cont][0]=j
                        p_reta01[2+cont][1]=y_var
                        cont=cont+1
            print("Variando eixo Y - p_reta01\n",p_reta01)
        #Organizando o array das posições=================
        #Deixando com o tamanho minimo
        p_reta01=p_reta01[:(2+cont)]
        tempx=0
        tempy=0
        #Faz a varredura no eixo X e ordena os pontos em ordem crescente
        for i in range(len(p_reta01)):
            for j in range(i+1,len(p_reta01)):
                if p_reta01[i][0] > p_reta01[j][0]:
                    tempx= p_reta01[i][0]
                    tempy= p_reta01[i][1]
                    p_reta01[i][0]=p_reta01[j][0]
                    p_reta01[i][1]=p_reta01[j][1]
                    p_reta01[j][0]=tempx
                    p_reta01[j][1]=tempy
        print("Array dos pontos ordenados:\n",p_reta01)
        print("Numero de Pontos encontrados.....",cont)
    #Atribui o quadrante que pertence os pontos da reta
    for n in range(len(p_reta01)):
        if 0<=p_reta01[n][0] and x1>p_reta01[n][0] and 0<=p_reta01[n][1] and y1>p_reta01[n][1]:
            p_reta01[n][2]=0
        elif x1<=p_reta01[n][0] and x2>p_reta01[n][0] and 0<=p_reta01[n][1] and y1>p_reta01[n][1]:
            p_reta01[n][2]=1
        elif x2<=p_reta01[n][0] and x3>=p_reta01[n][0] and 0<=p_reta01[n][1] and y1>p_reta01[n][1]:
            p_reta01[n][2]=2
        elif 0<=p_reta01[n][0] and x1>p_reta01[n][0] and y1<=p_reta01[n][1] and y2>p_reta01[n][1]:
            p_reta01[n][2]=3
        elif x1<=p_reta01[n][0] and x2>p_reta01[n][0] and y1<=p_reta01[n][1] and y2>p_reta01[n][1]:
            p_reta01[n][2]=4
        elif x2<=p_reta01[n][0] and x3>=p_reta01[n][0] and y1<=p_reta01[n][1] and y2>p_reta01[n][1]:
            p_reta01[n][2]=5
        elif 0<=p_reta01[n][0] and x1>p_reta01[n][0] and y2<=p_reta01[n][1] and y3>=p_reta01[n][1]:
            p_reta01[n][2]=6
        elif x1<=p_reta01[n][0] and x2>p_reta01[n][0] and y2<=p_reta01[n][1] and y3>=p_reta01[n][1]:
            p_reta01[n][2]=7
        elif x2<=p_reta01[n][0] and x3>=p_reta01[n][0] and y2<=p_reta01[n][1] and y3>=p_reta01[n][1]:
            p_reta01[n][2]=8
        else:
            p_reta01[n][2]=80
            print("Erro classificacao do quadrante")
    #Cria um array de calculo da distancia entre os pontos, utilizado para garantir que as distancias calculadas sejam atraladas ao quadrante correto
    p_reta01_calculo=np.zeros([2+(2*cont),3],dtype=int)
    repete=0
    for n in range(len(p_reta01)):
        if p_reta01[n][0]==x1 or p_reta01[n][0]==x2 or p_reta01[n][1]==y1 or p_reta01[n][1]==y2:
            p_reta01_calculo[n+repete][0]=p_reta01[n][0]
            p_reta01_calculo[n+repete][1]=p_reta01[n][1]
            p_reta01_calculo[n+repete][2]=p_reta01[n][2]
            p_reta01_calculo[n+1+repete][0]=p_reta01[n][0]
            p_reta01_calculo[n+1+repete][1]=p_reta01[n][1]
            p_reta01_calculo[n+1+repete][2]=p_reta01[n][2]
            repete=repete+1
        else:
            p_reta01_calculo[n+repete][0]=p_reta01[n][0]
            p_reta01_calculo[n+repete][1]=p_reta01[n][1]
            p_reta01_calculo[n+repete][2]=p_reta01[n][2]

    
    #Realiza os calculos de comprimento por quadrante
    dist_01=np.zeros([len(p_reta01)-1,2])
    for i in range(int(len(p_reta01_calculo)/2)):
        cateto_oposto=p_reta01_calculo[2*i][1]-p_reta01_calculo[(2*i)+1][1]
        cateto_adj=p_reta01_calculo[2*i][0]-p_reta01_calculo[(2*i)+1][0]
        dist_01[i][0]=(cateto_adj**2 + cateto_oposto**2)**0.5
        #Atribui o quadrante da medida calculada
        dist_01[i][1]=int(p_reta01[i][2])
    print("Distancias da Reta entre ponto %d e %d e o respectivo quadrante\n" %(inicial,final),dist_01)
    return dist_01

def pixel2mm(dist,calib,tipo=0):#Função para transformar a medida de pixel para cm e acordo com o array calibraçao
    #Tipo =0 - Eixo X - Tipo=1 - Eixo Y
    dist_final=0
    for n in range(len(dist)):
        if tipo==0:
            dist[n][0]=calib[int(dist[n][1])][0]*dist[n][0]
        else:
            dist[n][0]=calib[int(dist[n][1])][1]*dist[n][0]
        dist_final=dist_final+dist[n][0]
    print("O Array das distancias convertidas foi\n",dist)
    print("A distancia final foi de",dist_final)
    return dist_final
    
def calib_pixel(en_cam=True,Area=2000,lim_min_erro=10):
    while True:
        n_blocos=input("\nQuantos blocos padrão com alturas diferentes deseja utilizar ? (1 a 3)\n")
        if not n_blocos.isnumeric() or int(n_blocos)>3 or int(n_blocos)<0:
            print("------- !! Escolha valores de 1 a 3  !! ----------- ")
        else:
            n_blocos=int(n_blocos)
            break
    if en_cam:
        cap = cv2.VideoCapture(0)  # configuração da webcam  #1-webcam externa - 0-webcam notebook - para o raspberry cam -0
        sucess, img = cap.read()
        #Definindo os limites dos quadrantes em X
        x1=int(img.shape[1]/3)
        x2=int((2*img.shape[1])/3)
        x3=img.shape[1]

        #Definindo os limites dos quadrantes em Y
        y1=int(img.shape[0]/3)
        y2=int((2*img.shape[0])/3)
        y3=img.shape[0]
        
        #Declaro o vetor de saida das medidas encontradas em cada quadrante
        calib=np.empty([n_blocos,9,2])
        n_blocos_atual=0
        while n_blocos_atual<n_blocos:
            cont=0
            #Faz o loop nos 9 quadrantes
            while cont<9:
                verif_vazio= True
                if cont==0:
                    if n_blocos_atual !=0:
                        cap = cv2.VideoCapture(0)
                    print("Aperte Enter para ir para a próxima posição")
                    while True:
                        _, img = cap.read()
                        base=img.copy()
                        #Desenha os 9 quadrantes
                        cv2.line(base,(x1,0),(x1,y3),(0,255,0),2)
                        cv2.line(base,(x2,0),(x2,y3),(0,255,0),2)
                        cv2.line(base,(0,y1),(x3,y1),(0,255,0),2)
                        cv2.line(base,(0,y2),(x3,y2),(0,255,0),2)
                        #Destaca o Quadrante 1
                        cv2.line(base,(0,y1),(x1,y1),(0,0,255),2)
                        cv2.line(base,(x1,0),(x1,y1),(0,0,255),2)
                        #Apresenta ao usuario a referencia de posicionamento
                        cv2.imshow("Calibracao", base)
                        if cv2.waitKey(1) == 13: #Enter
                            #Obtem as medidas do aruco
                            ROI=img[0:y1,0:x1]
                            calib= aruco_measure(ROI,cont,n_blocos_atual,calib,Area)
                            print(calib)
                            if calib[n_blocos_atual][cont][0]<lim_min_erro or calib[n_blocos_atual][cont][1]<lim_min_erro:
                                print("Insira o aruco dentro da posição demarcada em vermelho")
                            else:
                                break               
                elif cont==1:
                    cap = cv2.VideoCapture(0)
                    print("Aperte Enter para ir para a próxima posição")
                    while True:
                        _, img = cap.read()
                        base=img.copy()
                        #Desenha os 9 quadrantes
                        cv2.line(base,(x1,0),(x1,y3),(0,255,0),2)
                        cv2.line(base,(x2,0),(x2,y3),(0,255,0),2)
                        cv2.line(base,(0,y1),(x3,y1),(0,255,0),2)
                        cv2.line(base,(0,y2),(x3,y2),(0,255,0),2)
                        #Destaca o Quadrante 2
                        cv2.line(base,(x1,0),(x1,y1),(0,0,255),2)
                        cv2.line(base,(x1,y1),(x2,y1),(0,0,255),2)
                        cv2.line(base,(x2,0),(x2,y1),(0,0,255),2)
                        #Apresenta ao usuario a referencia de posicionamento
                        cv2.imshow("Calibracao", base)
                        if cv2.waitKey(1) == 13: #Enter
                            #Obtem as medidas do aruco
                            ROI=img[0:y1,x1:x2]
                            calib= aruco_measure(ROI,cont,n_blocos_atual,calib,Area)
                            if calib[n_blocos_atual][cont][0]<lim_min_erro or calib[n_blocos_atual][cont][1]<lim_min_erro:
                                print("Insira o aruco dentro da posição demarcada em vermelho")
                            else:
                                break         
                elif cont==2:
                    cap = cv2.VideoCapture(0)
                    print("Aperte Enter para ir para a próxima posição")
                    while True:
                        _, img = cap.read()
                        base=img.copy()
                        #Desenha os 9 quadrantes
                        cv2.line(base,(x1,0),(x1,y3),(0,255,0),2)
                        cv2.line(base,(x2,0),(x2,y3),(0,255,0),2)
                        cv2.line(base,(0,y1),(x3,y1),(0,255,0),2)
                        cv2.line(base,(0,y2),(x3,y2),(0,255,0),2)
                        cv2.line(base,(x2,0),(x2,y1),(0,0,255),2)
                        cv2.line(base,(x2,y1),(x3,y1),(0,0,255),2)
                        #Apresenta ao usuario a referencia de posicionamento
                        cv2.imshow("Calibracao", base)
                        if cv2.waitKey(1) == 13: #Enter
                            #Obtem as medidas do aruco
                            ROI=img[0:y1,x2:x3]
                            calib= aruco_measure(ROI,cont,n_blocos_atual,calib,Area)
                            if calib[n_blocos_atual][cont][0]<lim_min_erro or calib[n_blocos_atual][cont][1]<lim_min_erro:
                                print("Insira o aruco dentro da posição demarcada em vermelho")
                            else:
                                break
                elif cont==3:
                    cap = cv2.VideoCapture(0)
                    print("Aperte Enter para ir para a próxima posição")
                    while True:
                        _, img = cap.read()
                        base=img.copy()
                        #Desenha os 9 quadrantes
                        cv2.line(base,(x1,0),(x1,y3),(0,255,0),2)
                        cv2.line(base,(x2,0),(x2,y3),(0,255,0),2)
                        cv2.line(base,(0,y1),(x3,y1),(0,255,0),2)
                        cv2.line(base,(0,y2),(x3,y2),(0,255,0),2)
                        cv2.line(base,(0,y1),(x1,y1),(0,0,255),2)
                        cv2.line(base,(x1,y1),(x1,y2),(0,0,255),2)
                        cv2.line(base,(0,y2),(x1,y2),(0,0,255),2)
                        #Apresenta ao usuario a referencia de posicionamento
                        cv2.imshow("Calibracao", base)
                        if cv2.waitKey(1) == 13: #Enter
                            #Obtem as medidas do aruco
                            ROI=img[y1:y2,0:x1]
                            calib= aruco_measure(ROI,cont,n_blocos_atual,calib,Area)
                            if calib[n_blocos_atual][cont][0]<lim_min_erro or calib[n_blocos_atual][cont][1]<lim_min_erro:
                                print("Insira o aruco dentro da posição demarcada em vermelho")
                            else:
                                break
                elif cont==4:
                    cap = cv2.VideoCapture(0)
                    print("Aperte Enter para ir para a próxima posição")
                    while True:
                        _, img = cap.read()
                        base=img.copy()
                        #Desenha os 9 quadrantes
                        cv2.line(base,(x1,0),(x1,y3),(0,255,0),2)
                        cv2.line(base,(x2,0),(x2,y3),(0,255,0),2)
                        cv2.line(base,(0,y1),(x3,y1),(0,255,0),2)
                        cv2.line(base,(0,y2),(x3,y2),(0,255,0),2)
                        cv2.line(base,(x1,y1),(x2,y1),(0,0,255),2)
                        cv2.line(base,(x2,y1),(x2,y2),(0,0,255),2)
                        cv2.line(base,(x1,y2),(x2,y2),(0,0,255),2)
                        cv2.line(base,(x1,y1),(x1,y2),(0,0,255),2)
                        #Apresenta ao usuario a referencia de posicionamento
                        cv2.imshow("Calibracao", base)
                        if cv2.waitKey(1) == 13: #Enter
                            #Obtem as medidas do aruco
                            ROI=img[y1:y2,x1:x2]
                            calib= aruco_measure(ROI,cont,n_blocos_atual,calib,Area)
                            if calib[n_blocos_atual][cont][0]<lim_min_erro or calib[n_blocos_atual][cont][1]<lim_min_erro:
                                print("Insira o aruco dentro da posição demarcada em vermelho")
                            else:
                                break
                elif cont==5:
                    cap = cv2.VideoCapture(0)
                    print("Aperte Enter para ir para a próxima posição")
                    while True:
                        _, img = cap.read()
                        base=img.copy()
                        #Desenha os 9 quadrantes
                        cv2.line(base,(x1,0),(x1,y3),(0,255,0),2)
                        cv2.line(base,(x2,0),(x2,y3),(0,255,0),2)
                        cv2.line(base,(0,y1),(x3,y1),(0,255,0),2)
                        cv2.line(base,(0,y2),(x3,y2),(0,255,0),2)
                        cv2.line(base,(x2,y1),(x3,y1),(0,0,255),2)
                        cv2.line(base,(x2,y1),(x2,y2),(0,0,255),2)
                        cv2.line(base,(x2,y2),(x3,y2),(0,0,255),2)
                        #Apresenta ao usuario a referencia de posicionamento
                        cv2.imshow("Calibracao", base)
                        if cv2.waitKey(1) == 13: #Enter
                            #Obtem as medidas do aruco
                            ROI=img[y1:y2,x2:x3]
                            calib= aruco_measure(ROI,cont,n_blocos_atual,calib,Area)
                            if calib[n_blocos_atual][cont][0]<lim_min_erro or calib[n_blocos_atual][cont][1]<lim_min_erro:
                                print("Insira o aruco dentro da posição demarcada em vermelho")
                            else:
                                break
                elif cont==6:
                    cap = cv2.VideoCapture(0)
                    print("Aperte Enter para ir para a próxima posição")
                    while True:
                        _, img = cap.read()
                        base=img.copy()
                        #Desenha os 9 quadrantes
                        cv2.line(base,(x1,0),(x1,y3),(0,255,0),2)
                        cv2.line(base,(x2,0),(x2,y3),(0,255,0),2)
                        cv2.line(base,(0,y1),(x3,y1),(0,255,0),2)
                        cv2.line(base,(0,y2),(x3,y2),(0,255,0),2)
                        cv2.line(base,(0,y2),(x1,y2),(0,0,255),2)
                        cv2.line(base,(x1,y2),(x1,y3),(0,0,255),2)
                        #Apresenta ao usuario a referencia de posicionamento
                        cv2.imshow("Calibracao", base)
                        if cv2.waitKey(1) == 13: #Enter
                            #Obtem as medidas do aruco
                            ROI=img[y2:y3,0:x1]
                            calib= aruco_measure(ROI,cont,n_blocos_atual,calib,Area)
                            if calib[n_blocos_atual][cont][0]<lim_min_erro or calib[n_blocos_atual][cont][1]<lim_min_erro:
                                print("Insira o aruco dentro da posição demarcada em vermelho")
                            else:
                                break
                elif cont==7:
                    cap = cv2.VideoCapture(0)
                    print("Aperte Enter para ir para a próxima posição")
                    while True:
                        _, img = cap.read()
                        base=img.copy()
                        #Desenha os 9 quadrantes
                        cv2.line(base,(x1,0),(x1,y3),(0,255,0),2)
                        cv2.line(base,(x2,0),(x2,y3),(0,255,0),2)
                        cv2.line(base,(0,y1),(x3,y1),(0,255,0),2)
                        cv2.line(base,(0,y2),(x3,y2),(0,255,0),2)
                        cv2.line(base,(x1,y2),(x2,y2),(0,0,255),2)
                        cv2.line(base,(x1,y2),(x1,y3),(0,0,255),2)
                        cv2.line(base,(x2,y2),(x2,y3),(0,0,255),2)
                        #Apresenta ao usuario a referencia de posicionamento
                        cv2.imshow("Calibracao", base)
                        if cv2.waitKey(1) == 13: #Enter
                            #Obtem as medidas do aruco
                            ROI=img[y2:y3,x1:x2]
                            calib= aruco_measure(ROI,cont,n_blocos_atual,calib,Area)
                            if calib[n_blocos_atual][cont][0]<lim_min_erro or calib[n_blocos_atual][cont][1]<lim_min_erro:
                                print("Insira o aruco dentro da posição demarcada em vermelho")
                            else:
                                break
                else:
                    cap = cv2.VideoCapture(0)
                    print("Aperte Enter para ir para a próxima posição")
                    while True:
                        _, img = cap.read()
                        base=img.copy()
                        #Desenha os 9 quadrantes
                        cv2.line(base,(x1,0),(x1,y3),(0,255,0),2)
                        cv2.line(base,(x2,0),(x2,y3),(0,255,0),2)
                        cv2.line(base,(0,y1),(x3,y1),(0,255,0),2)
                        cv2.line(base,(0,y2),(x3,y2),(0,255,0),2)
                        cv2.line(base,(x2,y2),(x3,y2),(0,0,255),2)
                        cv2.line(base,(x2,y2),(x2,y3),(0,0,255),2)
                        #Apresenta ao usuario a referencia de posicionamento
                        cv2.imshow("Calibracao", base)
                        if cv2.waitKey(1) == 13: #Enter
                            #Obtem as medidas do aruco
                            ROI=img[y2:y3,x2:x3]
                            calib= aruco_measure(ROI,cont,n_blocos_atual,calib,Area)
                            if calib[n_blocos_atual][cont][0]<lim_min_erro or calib[n_blocos_atual][cont][1]<lim_min_erro:
                                print("Insira o aruco dentro da posição demarcada em vermelho")
                            else:
                                print("Aperte Espaço para continuar")
                                cap.release()  # desativa webcam
                                break
                        
                cont=cont+1
                if cv2.waitKey(1) == 32:#Se aperta espaço
                    break
                cap.release()  # desativa webcam
            n_blocos_atual=n_blocos_atual+1
    cap.release()  # desativa webcam
    print(calib)
    while True:
        altura=input('\nInsira a altura do aruco em milimetros:   ')
        largura=input('\nInsira a largura do aruco em milimetros:   ')
        if not altura.isnumeric():
            print("Valor de altura inserido não é um numero")
        if not largura.isnumeric():
            print("Valor de largura inserido não é um numero")
        else:
            largura=float(largura)
            altura=float(altura)
            break
    for i in range(n_blocos):
        for j in range(len(calib[0])):
            calib[i][j][0]=largura/calib[i][j][0]
            calib[i][j][1]=altura/calib[i][j][1]
    px_calib=np.empty([9,2])
    for j in range(len(calib[0])):
        print("j ",j)
        px_calib[j][0]=0
        px_calib[j][1]=0
        for i in range(n_blocos):
            px_calib[j][0]=px_calib[j][0]+calib[i][j][0]
            px_calib[j][1]=px_calib[j][1]+calib[i][j][1]
        px_calib[j][0]=px_calib[j][0]/n_blocos
        px_calib[j][1]=px_calib[j][1]/n_blocos
    print("O valor mm/px é")
    print(px_calib)
    calib_ok=True
    arq=open('arquivo.pck','wb')
    pickle.dump(px_calib,arq)
    arq.close()
    return px_calib

def detect_circles(img,minD=300,HThrs=255,LThrs=30,minR=10):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    bluered_img=cv2.medianBlur(gray,5)
    #circles retorna a coordenada do centro e o raio --- [x , y , raio]
    circles=cv2.HoughCircles(image=bluered_img,method=cv2.HOUGH_GRADIENT,dp=1,minDist=minD,param1=HThrs,param2=LThrs,minRadius=minR,maxRadius=0)
    if circles is None:
        print("-------- Não foram encontrados circunferências na imagem ---------")
        #circle_points=np.zeros([1,2,2],dtype=int)
        return None,None
    else:
        circle_points=np.zeros([len(circles[0]),2,2],dtype=int)
        for i in range(len(circles[0])):
            px1=int(circles[0][i][0])
            px2=int(circles[0][i][0])
            py1=int(circles[0][i][1]-circles[0][i][2])
            py2=int(circles[0][i][1]+circles[0][i][2])
            circle_points[i][0][0]=px1
            circle_points[i][0][1]=py1
            circle_points[i][1][0]=px2
            circle_points[i][1][1]=py2
    return circle_points,circles

    
    
    