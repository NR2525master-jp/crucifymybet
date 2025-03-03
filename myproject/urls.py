from django.contrib import admin
from django.urls import path
from myapp import views
from django.views.generic import RedirectView
from myapp.views import predict
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='home'),  # homeビューを表示
    path('admin/', admin.site.urls),
    path("predict/", predict),
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico", permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# 開発環境のみ debug_toolbar を有効化
if settings.DEBUG:
    import debug_toolbar
    if "__debug__/" not in urlpatterns:
        urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]