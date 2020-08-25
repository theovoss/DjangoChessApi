from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('DjangoChessApi.Chess.urls', namespace='Chess')),
    path('api/', include('DjangoChessApi.api.urls')),
    path('admin/', admin.site.urls),
    path('grappelli/', include('grappelli.urls')),
    # Accounts
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('django_registration.backends.one_step.urls')),
]
