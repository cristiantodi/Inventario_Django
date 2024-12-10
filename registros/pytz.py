from django.utils.timezone import make_aware
from registro.models import RegistroVenta
import pytz

# Ajusta según tu zona horaria
tz = pytz.timezone('America/Mexico_City')

for venta in RegistroVenta.objects.all():
    if venta.fecha.tzinfo is None:  # Si es naive
        venta.fecha = make_aware(venta.fecha, tz)
        venta.save()
