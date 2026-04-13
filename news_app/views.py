from django.shortcuts import render, get_object_or_404, redirect
from .models import POST, CATEGORY
from django.db.models import Q

# ====================== HOME ======================
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


# ====================== CHI TIẾT ======================
def post_detail(request, id):
    BAIVIET = get_object_or_404(POST, id=id)

    return render(request, 'post_detail.html', {
        'BAIVIET': BAIVIET
    })


# ====================== AUTH ======================
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm   # 👈 dùng form custom (cho phép pass đơn giản)


# ====================== REGISTER ======================
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()   # 👉 email sẽ được lưu nếu form đúng
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


# ====================== LOGIN ======================
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
            error = '❌ Sai tên đăng nhập hoặc mật khẩu'

    return render(request, 'login.html', {'error': error})


# ====================== LOGOUT ======================
def logout_view(request):
    if request.method == 'POST':   # 👈 FIX lỗi 405
        logout(request)
        return redirect('home')

    return redirect('home')

