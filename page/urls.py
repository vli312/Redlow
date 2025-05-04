from django.urls import path
from . import views
app_name = 'page'
urlpatterns = [
    # page views
    path('', views.homeview, name='homeview'),
    path('about/', views.aboutview, name='aboutview'),
    path('product/', views.productview, name='productview'),
    path('design/', views.neighbourhoodview, name='neighbourhoodview'),
    path('review/', views.reviewview, name='reviewview'),
    path('privacy/', views.privacyview, name='privacyview'),
    path('faq/', views.faqview, name='faqview'),
    path('contact/', views.contactview, name='contactview'),
    path('product/zipcodemap.html', views.zipcodemapview, name='zipcodemapview'),
    path('design/neighbourhoodmap.html', views.neighbourhoodmapview, name='neighbourhoodmapview'),
]