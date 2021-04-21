from django.contrib import admin
from django.urls import path, include
from bot import urls as bot

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(bot)),
]
