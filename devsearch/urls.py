from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from django.conf.urls.static import static

urlpatterns = [
    path('project/',include(('projects.urls','projects'))),
    path('admin/', admin.site.urls),
    path('',include(('users.urls','users')))
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)