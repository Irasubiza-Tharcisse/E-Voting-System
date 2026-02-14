from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from users import views

urlpatterns = [
    path('', views.home_view, name='home'),       # ✅ root URL
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # users app urls
    path('elections/', include('elections.urls')),
    path('admin-portal/', include('adminpanel.urls')),


    # Two-factor auth URLs
    #path('account/', include('two_factor.urls')),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
