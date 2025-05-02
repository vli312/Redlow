from django.urls import path
from . import views
app_name = 'page'
urlpatterns = [
    # page views
    path('', views.homeview, name='homeview'),
    path('about/', views.aboutview, name='aboutview'),
    path('product/', views.productview, name='productview'),
<<<<<<< HEAD
=======
    path('design/', views.designview, name='designview'),
>>>>>>> 8cffef8490a4ab850ae3af9b1d1b3f2bca8e328a
    path('review/', views.reviewview, name='reviewview'),
    path('privacy/', views.privacyview, name='privacyview'),
    path('faq/', views.faqview, name='faqview'),
    path('contact/', views.contactview, name='contactview'),
<<<<<<< HEAD
=======
    path('product/zipcodemap.html', views.zipcodemapview, name='zipcodemapview'),
    path('design/neighbourhoodmap.html', views.neighbourhoodmapview, name='neighbourhoodmapview'),
>>>>>>> 8cffef8490a4ab850ae3af9b1d1b3f2bca8e328a
]