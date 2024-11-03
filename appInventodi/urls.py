from django.urls import path
from appInventodi import views
from .views import lista_productos,contactanos

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="Home"),
    path('busqueda/', lista_productos, name='filtrar'),
    path('contactanos/', views.contactanos, name='contactanos'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)