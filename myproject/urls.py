from django.contrib import admin
from django.urls import path
from myapp import views
from django.views.generic import RedirectView
from myapp.views import predict
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # homeビューを表示
    path('admin/', admin.site.urls),
    path("predict/", predict),
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico", permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
