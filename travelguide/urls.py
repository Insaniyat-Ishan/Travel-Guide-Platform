
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import RedirectView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', RedirectView.as_view(pattern_name='home', permanent=False)),
    path('',include('tbp.urls')),
    
]
