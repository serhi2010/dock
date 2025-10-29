from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Advertisement
from .forms import AdvertisementForm, CommentForm

@login_required
def advertisement_list(request):
    advertisements = Advertisement.objects.order_by('-created_at')
    return render(request, 'advertisement/advertisement_list.html', {'advertisements': advertisements})

@login_required
def advertisement_create(request):
    if not (request.user.role == 'teacher' or request.user.role == 'admin' or request.user.is_staff):
        return HttpResponseForbidden("⛔ Лише вчителі та адміністратори можуть створювати оголошення.")

    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('advertisement:advertisement_list')
    else:
        form = AdvertisementForm()
    return render(request, 'advertisement/advertisement_create.html', {'form': form})

@login_required
def advertisement_detail(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk)
    comments = ad.comments.order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.advertisement = ad
            comment.author = request.user
            comment.save()
            return redirect('advertisement:advertisement_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'advertisement/advertisement_detail.html', {
        'ad': ad,
        'comments': comments,
        'form': form
    })
