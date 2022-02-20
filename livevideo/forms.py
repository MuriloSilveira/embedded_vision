from django import forms
from django.core.validators import MinValueValidator
from .models import Calibracao
from .models import Medida
import datetime

# iterable
CAM_CHOICES = (
    ("1", "Raspberry Pi Cam"),
    ("2", "Logitech C270"),
    ("3", "Outra"),
)

AMOSTRA_CHOICES = (
    ("1", 1),
    ("2", 2),
    ("3", 3),
)

STATUS_CHOICES = (
    ("1", "Sistema Ativo"),
    ("2", "Sistema em Falha"),
    ("3", "Sistema Desligado"),
)

passa_data='2021-11-03'

class JobForm(forms.Form):
    lote = forms.IntegerField(label='Lote', validators=[MinValueValidator(1)])
    max_valor_x = forms.DecimalField(label='Limite Máximo Medida Eixo X (mm)', decimal_places=2, max_digits=5,
                                     validators=[MinValueValidator(0.0)])
    min_valor_x = forms.DecimalField(label='Limite Mínimo Medida Eixo X (mm)', decimal_places=2, max_digits=5,
                                     validators=[MinValueValidator(0.0)])
    max_valor_y = forms.DecimalField(label='Limite Máximo Medida Eixo Y (mm)', decimal_places=2, max_digits=5,
                                     validators=[MinValueValidator(0.0)])
    min_valor_y = forms.DecimalField(label='Limite Mínimo Medida Eixo Y (mm)', decimal_places=2, max_digits=5,
                                     validators=[MinValueValidator(0.0)])
    camera = forms.ChoiceField(label='Câmera', choices=CAM_CHOICES)
    #"""
    calibs = Calibracao.objects.all()
    cont = 0
    lista_calib=[]
    for i in calibs:
        cont=cont+1
        lista_calib.append((str(cont),i.nome))
    calibracao = forms.ChoiceField(label='Dados de Calibração', choices=lista_calib)
    #"""

class QueryDayForm(forms.Form):
    global passa_data
    #"""
    medidas=Medida.objects.all()
    cont = 1
    lista_medidas=[]
    lista_datas=[]
    for i in medidas:
        t=i.data
        dado=t.strftime('%Y-%m-%d')
        if dado not in lista_datas:
            lista_datas.append(dado)
            lista_medidas.append((str(cont),dado))
            cont=cont+1
    print("Lista medidas eh ")
    print(lista_medidas)
    dia = forms.ChoiceField(label='Data', choices=lista_medidas)
    passa_data=dia
    #"""
    
class QueryLoteForm(forms.Form):
    #"""
    print("passsa data eh")
    print(passa_data)
    medidas=Medida.objects.filter(data='2021-11-03')
    cont = 1
    lista_medidas=[]
    lista_lotes=[]
    for i in medidas:
        dado=i.lote
        if dado not in lista_lotes:
            lista_lotes.append(dado)
            lista_medidas.append((str(cont),dado))
            cont=cont+1
    lote = forms.ChoiceField(label='Lote', choices=lista_medidas)
    #"""


class CalibForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=20, min_length=3)
    camera = forms.ChoiceField(label='Câmera', choices=CAM_CHOICES)
    n_amost = forms.ChoiceField(label='Nº de Amostras', choices=AMOSTRA_CHOICES)
    
    
class ResCalibForm(forms.Form):
    altura=forms.DecimalField(label='Altura da Amostra (mm)', decimal_places=2, max_digits=5,
                                     validators=[MinValueValidator(0.1)])
    largura=forms.DecimalField(label='Largura da Amostra (mm)', decimal_places=2, max_digits=5,
                                     validators=[MinValueValidator(0.1)])

class DisplayForm(forms.Form):
    lote = forms.IntegerField(label='Lote', validators=[MinValueValidator(1)])
    max_valor_x = forms.DecimalField(label='Valor Máximo Eixo X', decimal_places=2, max_digits=5)
    min_valor_x = forms.DecimalField(label='Valor Mínimo Eixo X', decimal_places=2, max_digits=5)
    max_valor_y = forms.DecimalField(label='Valor Máximo Eixo Y', decimal_places=2, max_digits=5)
    min_valor_y = forms.DecimalField(label='Valor Mínimo Eixo Y', decimal_places=2, max_digits=5)
    status = forms.ChoiceField(label='Status', choices=STATUS_CHOICES)
    med_valor_x = forms.DecimalField(label='Valor Médio Eixo X', decimal_places=2, max_digits=5)
    med_valor_y = forms.DecimalField(label='Valor Médio Eixo Y', decimal_places=2, max_digits=5)
