from django.urls import path
from appInventodi import views
from .views import lista_productos

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="Home"),
    path('productos/', lista_productos, name='filtrar'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)