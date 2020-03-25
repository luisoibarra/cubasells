from datetime import datetime,
from core.models import Server, FileToBackup, Result, ServerGroup,
#UTILIZAR LOS MODELOS DE LA BD
import django_excel as excel

"""Cambiar el URL para recibir un format exp y distinguir el formato a exportar"""
# urlpatterns = [
#     path('admin/',             admin.site.urls),

#     # Paths for results view and announces
#     path('results/',                        views.listresults),
#  """"   path('results/export/<str:format_exp>', views.listresults),  """"


def listresults(request, format_exp=None):
    export = []
    # Se agregan los encabezados de las columnas
    export.append([
        'date',
        'group',
        'server',

        # Se obtienen los datos de la tabla o model y se agregan al array
        results=Result.objects.all()
        for result in results:
        # ejemplo para dar formato a fechas, estados (si/no, ok/fail) o
        # acceder a campos con relaciones y no solo al id
        export.append([
            "{0:%Y-%m-%d %H:%M}".format(result.date),
            result.hostname_id.group.groupname,
            result.hostname_id,
        ])

        # Obtenemos la fecha para agregarla al nombre del archivo
        today=datetime.now()
        strToday=today.strftime("%Y%m%d")

        # se transforma el array a una hoja de calculo en memoria
        sheet=excel.pe.Sheet(export)

        # se devuelve como "Response" el archivo para que se pueda "guardar"
        # en el navegador, es decir como hacer un "Download"
        if format_exp == "csv":
            return excel.make_response(sheet, "csv", file_name="results-"+strToday+".csv")
        elif format_exp == "ods":
            return excel.make_response(sheet, "ods", file_name="results-"+strToday+".ods")
        elif format_exp == "xlsx":
            return excel.make_response(sheet, "xlsx", file_name="results-"+strToday+".xlsx")
        else:
            #messages.error(request, 'Export format {} not supported'.format(format_exp))
            # MENSAJE DE ERROR POR FORMATO INVALIDO
