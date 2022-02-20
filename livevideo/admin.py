from django.contrib import admin
from .models import Medida
from .models import Calibracao 
from import_export.admin import ImportExportMixin

class MedidaAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ('id', 'lote', 'valor_x', 'valor_y', 'data', 'horario')


admin.site.register(Medida, MedidaAdmin)


class CalibAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ('id', 'nome', 'n_amostra', 'val_x1', 'val_y1', 'val_x2', 'val_y2', 'val_x3', 'val_y3', 'val_x4', 'val_y4', 'val_x5', 'val_y5', 'val_x6', 'val_y6', 'val_x7', 'val_y7', 'val_x8', 'val_y8', 'val_x9', 'val_y9')


admin.site.register(Calibracao, CalibAdmin)

#class MedidaExport(ImportExportModelAdmin):
#    pass

#class CalibExport(ImportExportModelAdmin):
#    pass