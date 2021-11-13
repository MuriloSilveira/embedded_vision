from django.db import models


class Medida(models.Model):
    id = models.BigAutoField(primary_key=True)
    lote = models.PositiveSmallIntegerField('Lote')
    valor_x = models.DecimalField('Medida Eixo X', decimal_places=2, max_digits=5)
    valor_y = models.DecimalField('Medida Eixo Y', decimal_places=2, max_digits=5)
    data = models.DateField('Data', auto_now=True)
    horario = models.TimeField('Horário', auto_now=True)

    def __str__(self):
        return f'{self.id}'


class Calibracao(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField('Nome', max_length=20)
    n_amostra = models.PositiveSmallIntegerField('N° de Amostras')
    val_x1 = models.DecimalField('Medida 1 Eixo X', decimal_places=6, max_digits=8)
    val_y1 = models.DecimalField('Medida 2 Eixo Y', decimal_places=6, max_digits=8)
    val_x2 = models.DecimalField('Medida 2 Eixo X', decimal_places=6, max_digits=8)
    val_y2 = models.DecimalField('Medida 2 Eixo Y', decimal_places=6, max_digits=8)
    val_x3 = models.DecimalField('Medida 3 Eixo X', decimal_places=6, max_digits=8)
    val_y3 = models.DecimalField('Medida 3 Eixo Y', decimal_places=6, max_digits=8)
    val_x4 = models.DecimalField('Medida 4 Eixo X', decimal_places=6, max_digits=8)
    val_y4 = models.DecimalField('Medida 4 Eixo Y', decimal_places=6, max_digits=8)
    val_x5 = models.DecimalField('Medida 5 Eixo X', decimal_places=6, max_digits=8)
    val_y5 = models.DecimalField('Medida 5 Eixo Y', decimal_places=6, max_digits=8)
    val_x6 = models.DecimalField('Medida 6 Eixo X', decimal_places=6, max_digits=8)
    val_y6 = models.DecimalField('Medida 6 Eixo Y', decimal_places=6, max_digits=8)
    val_x7 = models.DecimalField('Medida 7 Eixo X', decimal_places=6, max_digits=8)
    val_y7 = models.DecimalField('Medida 7 Eixo Y', decimal_places=6, max_digits=8)
    val_x8 = models.DecimalField('Medida 8 Eixo X', decimal_places=6, max_digits=8)
    val_y8 = models.DecimalField('Medida 8 Eixo Y', decimal_places=6, max_digits=8)
    val_x9 = models.DecimalField('Medida 9 Eixo X', decimal_places=6, max_digits=8)
    val_y9 = models.DecimalField('Medida 9 Eixo Y', decimal_places=6, max_digits=8)

    def __str__(self):
        return self.nome