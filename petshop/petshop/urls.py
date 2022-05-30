from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('animalcart.urls', namespace='animalcart')),
    path('order/', include('animalorders.urls', namespace='animalorders')),
    path('payment/', include('gateways.urls', namespace='gateways')),
    path("", include('animalshop.urls', namespace='animalshop'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
