from django.shortcuts import render, get_object_or_404
from .models import POST, CATEGORY
from django.db.models import Q

def home_view(request):

    TU_KHOA = request.GET.get('q', '')

    LIST_DANHMUC = CATEGORY.objects.all()

    if TU_KHOA:
        DANHSACH_BAIVIET = POST.objects.filter(
            Q(TITLE__icontains=TU_KHOA) |
            Q(BAIVIET__NAME__icontains=TU_KHOA)
        ).order_by('-NGAYDANG')
    else:
        DANHSACH_BAIVIET = POST.objects.all().order_by('-NGAYDANG')


    context = {
        'DANHSACH_BAIVIET': DANHSACH_BAIVIET,
        'TU_KHOA': TU_KHOA,
        'LIST_DANHMUC': LIST_DANHMUC
    }

    return render(request, 'home.html', context)

def post_detail(request, id):
    BAIVIET = get_object_or_404(POST, id=id)

    context = {
        'BAIVIET': BAIVIET
    }

    return render(request, 'post_detail.html', context)
