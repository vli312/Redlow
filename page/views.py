from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from page.models import Review
from page.models import Region
from users.models import User

# Create your views here.
def homeview(request):
    return render(request,
                  'page/page_story/index.html')

def aboutview(request):
    return render(request,
                  'page/page_story/about.html')

def reviewview(request):
    reviews = Review.objects.select_related('user', 'region').order_by('-created_at')
    regions = Region.objects.all().order_by('region_name')

    if request.method == 'POST':
        if request.POST.get('submit') == 'Add':
            try:
                user = User.objects.get(username=request.session.get('username'))
                region_id = int(request.POST.get('region_id'))
                region = Region.objects.get(region_id=region_id)
                content = request.POST.get('text', '').strip()
                rating = int(request.POST.get('rating', 1))
                num_bedrooms = int(request.POST.get('num_bedrooms', 0))
                num_bathrooms = int(request.POST.get('num_bathrooms', 0))
                price_paid = float(request.POST.get('price_paid', 0))
                ownership_status = request.POST.get('ownership_status')
                zip_code = request.POST.get('zip_code', '')

                Review.objects.create(
                    user=user,
                    region=region,
                    content=content,
                    rating=rating,
                    num_bedrooms=num_bedrooms,
                    num_bathrooms=num_bathrooms,
                    price_paid=price_paid,
                    ownership_status=ownership_status,
                    zip_code=zip_code
                )

                messages.success(request, "Review added successfully!")
                return redirect('page:reviewview')
            except Exception as e:
                messages.error(request, f"Failed to add review: {e}")

        elif request.POST.get('submit') == 'Delete':
            review_id = request.POST.get('review_id')
            review = get_object_or_404(Review, pk=review_id)
            review.delete()
            messages.warning(request, "Review deleted.")
            return redirect('page:reviewview')

    return render(request, 'page/page_story/review.html', {
        'reviews': reviews,
        'regions': regions
    })

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
