from django.urls import include, path
from django.conf.urls import url

from .views import Home,DataAnalysis
from django.conf import settings
from django.conf.urls.static import static

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'Home',Home.as_view(),name="Home"),#
    url(r'DataAnalysis',DataAnalysis.as_view(),name="DataAnalysis")
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)