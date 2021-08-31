from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('saving/', include('savings.urls')),
    path('loan/', include('loan.urls')),
    path('superadmin/', include('superadmin.urls')),
]
