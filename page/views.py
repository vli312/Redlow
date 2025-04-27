from django.shortcuts import render, redirect
from .models import regular_user, admin_user
from django.views.decorators.clickjacking import xframe_options_exempt

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

def login(request):
    username = request.POST.get("username")
    pw = request.POST.get("pw")
    # authentication with password for regular user
    if (username == regular_user['username'] and pw == regular_user['pw']):
        # identification with sessions
        request.session['username'] = username
        request.session['role'] = 'regular'
        return redirect('page:homeview')
    # admin authentication
    elif (username == admin_user['username'] and pw == admin_user['pw']):
        request.session['username'] = username
        request.session['role'] = 'admin'
        return redirect('page:homeview')
    else:
        return redirect('page:homeview')

def logout(request):
    del request.session['username']
    del request.session['role']
    return redirect('page:homeview')

@xframe_options_exempt
def zipcodemapview(request):
    return render(request,
                  'page/page_story/folium_map_zipcode.html')

@xframe_options_exempt
def neighbourhoodmapview(request):
    return render(request,
                  'page/page_story/folium_map_neighbourhood.html')