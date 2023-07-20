
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    path('ezystores-admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path('', include("core.urls")),
    path('accounts/', include("allauth.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'