from django.shortcuts import render, redirect
from .models import regular_user, admin_user
from users.models import User

# Create your views here.
def homeview(request):
    return render(request,
                  'page/page_story/index.html')

def aboutview(request):
    return render(request,
                  'page/page_story/about.html')

def designview(request):
    return render(request,
                  'page/page_story/design.html')

def productview(request):
    return render(request,
                  'page/page_story/product.html')

def privacyview(request):
    return render(request,
                  'page/page_story/privacy.html')

def faqview(request):
    return render(request,
                  'page/page_story/faq.html')

def contactview(request):
    return render(request,
                  'page/page_story/contact.html')
