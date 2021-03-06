# Generated by Django 3.2.8 on 2021-11-03 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livevideo', '0004_alter_calibracao_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calibracao',
            name='val_x1',
            field=models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Medida 1 Eixo X'),
        ),
        migrations.AlterField(
            model_name='calibracao',
            name='val_x2',
            field=models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Medida 2 Eixo X'),
        ),
        migrations.AlterField(
            model_name='calibracao',
            name='val_x3',
            field=models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Medida 3 Eixo X'),
        ),
        migrations.AlterField(
            model_name='calibracao',
            name='val_x4',
            field=models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Medida 4 Eixo X'),
        ),
        migrations.AlterField(
            model_name='calibracao',
            name='val_x5',
            field=models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Medida 5 Eixo X'),
        ),
        migrations.AlterField(
            model_name='calibracao',
            name='val_x6',
            field=models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Medida 6 Eixo X'),
        ),
        migrations.AlterField(
            model_name='calibracao',
            name='val_x7',
            field=models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Medida 7 Eixo X'),
        ),
        migrations.AlterField(
            model_name='calibracao',
            name='val_x8',
            field=models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Medida 8 Eixo X'),
        ),
        migrations.AlterField(
            model_name='calibracao',
            name='val_x9',
            field=models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Medida 9 Eixo X'),
        ),
        migrations.AlterField(
            model_name='calibracao',
            name='val_y1',
            field=models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Medida 2 Eixo Y'),
        ),
        migrations.AlterField(
            model_name='calibracao',
            name='val_y2',
            field=models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Medida 2 Eixo Y'),
        ),
        migrations.AlterField(
            model_name='calibracao',
            name='val_y3',
            field=models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Medida 3 Eixo Y'),
        ),
        migrations.AlterField(
            model_name='calibracao',
            name='val_y4',
            field=models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Medida 4 Eixo Y'),
        ),
        migrations.AlterField(
            model_name='calibracao',
            name='val_y5',
            field=models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Medida 5 Eixo Y'),
        ),
        migrations.AlterField(
            model_name='calibracao',
            name='val_y6',
            field=models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Medida 6 Eixo Y'),
        ),
        migrations.AlterField(
            model_name='calibracao',
            name='val_y7',
            field=models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Medida 7 Eixo Y'),
        ),
        migrations.AlterField(
            model_name='calibracao',
            name='val_y8',
            field=models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Medida 8 Eixo Y'),
        ),
        migrations.AlterField(
            model_name='calibracao',
            name='val_y9',
            field=models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Medida 9 Eixo Y'),
        ),
    ]
