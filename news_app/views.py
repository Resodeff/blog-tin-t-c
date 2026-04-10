from django.shortcuts import render, get_object_or_404, redirect
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

#code của Truyền ở đây
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = 'Sai tên đăng nhập hoặc mật khẩu'

    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('home')

#==================================================================