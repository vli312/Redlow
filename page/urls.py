from django.urls import path
from . import views
app_name = 'page'
urlpatterns = [
    # page views
    path('', views.homeview, name='homeview'),
    path('about/', views.aboutview, name='aboutview'),
    path('product/', views.productview, name='productview'),
    path('design/', views.designview, name='designview'),
    path('privacy/', views.privacyview, name='privacyview'),
    path('faq/', views.faqview, name='faqview'),
    path('contact/', views.contactview, name='contactview'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]