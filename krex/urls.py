"""
URL configuration for krex project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from krexapp import views  # 👈 import views

urlpatterns = [

    # Default Django admin
    path('admin/', admin.site.urls),

    # 🔥 FORCE ROLE SELECTION AS ROOT
    path('', views.select_role, name='root'),

    # All other app URLs
    path('', include('krexapp.urls')),

]

# Media serving
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)