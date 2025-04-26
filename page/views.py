from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from comments.models import Comment
from users.models import User

# Create your views here.
def homeview(request):
    return render(request,
                  'page/page_story/index.html')

def aboutview(request):
    return render(request,
                  'page/page_story/about.html')

def reviewview(request):
    comments = Comment.objects.order_by('-created')
    if request.method == 'POST':
        if 'text' in request.POST:
            userFK = User.objects.get(username=request.session.get('username'))
            comment_text = request.POST.get('text')
            new_comment = Comment.objects.create(
                user=userFK,
                zipCode=22201,
                text=comment_text,
            )
            new_comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment added')
            return redirect('page:reviewview')
        elif 'Delete' in request.POST.get('submit'):
            comment_id = request.POST.get('comment_id')
            if comment_id:
                comment = get_object_or_404(Comment, pk=comment_id)
                comment.delete()
                userFK = User.objects.get(username=request.session.get('username'))
                messages.add_message(request, messages.WARNING, f'You successfully deleted a comment')
                return redirect('page:reviewview')
            else:
                print("Error: comment_id is None")
    return render(request,
                  'page/page_story/review.html',{'comments':comments})

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
