from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
from .views import file_list, download_file



sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns =[
    # path('/', views.register, name='register'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', file_list, name='file_list'),
    path('download/<int:file_id>/', download_file, name='download_file'),
]

