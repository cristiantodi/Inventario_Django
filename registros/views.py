from django.shortcuts import render
from django.db.models import Sum
from registros.models import RegistroVenta
from django.utils import timezone
from django.utils.timezone import now, timedelta
import json
from datetime import datetime, timedelta

# def graficar_ventas(request):
#     # Filtrar las ventas de los últimos 7 días
#     hoy = timezone.now()  # Ahora con soporte de zona horaria
#     hace_una_semana = hoy - timedelta(days=7)

#     ventas = RegistroVenta.objects.filter(fecha__range=[hace_una_semana, hoy])

#     # Agrupar por día y sumar valores
#     ventas_por_dia = ventas.extra(select={'day': "DATE(fecha)"}).values('day').annotate(total=Sum('valor'))

#     contexto = {
#         'ventas_por_dia': ventas_por_dia,
#     }
#     return render(request, 'registro.html', contexto)

def graficar_ventas(request):
    hoy = now()
    hace_una_semana = hoy - timedelta(days=7)

    ventas = RegistroVenta.objects.filter(fecha__range=[hace_una_semana, hoy])
    ventas_por_dia = (
        ventas.extra(select={'day': "DATE(fecha)"})
        .values('day')
        .annotate(total=Sum('valor'))
    )

    # Convierte ventas_por_dia a JSON serializable
    ventas_por_dia_json = json.dumps(list(ventas_por_dia))

    contexto = {
        'ventas_por_dia': ventas_por_dia_json,  # Enviar JSON serializado al template
    }
    return render(request, 'registro.html', contexto)