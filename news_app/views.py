from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import DangKyForm, DangNhapForm, PostForm
from .models import CATEGORY, POST


def shared_context(tu_khoa=""):
    return {
        "LIST_DANHMUC": CATEGORY.objects.all(),
        "TU_KHOA": tu_khoa,
    }


def user_can_manage_post(request, bai_viet):
    return request.user.is_authenticated and bai_viet.TACGIA_id == request.user.id


# ====================== HOME ======================
def home_view(request):
    tu_khoa = request.GET.get("q", "").strip()

    danh_sach_bai_viet = POST.objects.select_related("TACGIA", "BAIVIET").order_by(
        "-NGAYDANG"
    )
    if tu_khoa:
        danh_sach_bai_viet = danh_sach_bai_viet.filter(
            Q(TITLE__icontains=tu_khoa) | Q(BAIVIET__NAME__icontains=tu_khoa)
        )

    context = shared_context(tu_khoa)
    context["DANHSACH_BAIVIET"] = danh_sach_bai_viet
    return render(request, "home.html", context)



# ====================== CHI TIẾT ======================
def post_detail(request, id):
    bai_viet = get_object_or_404(
        POST.objects.select_related("TACGIA", "BAIVIET").prefetch_related("THELOAI"),
        id=id,
    )

    context = shared_context()
    context.update(
        {
            "BAIVIET": bai_viet,
            "CO_THE_QUAN_LY": user_can_manage_post(request, bai_viet),
        }
    )
    return render(request, "post_detail.html", context)


# ====================== LOGIN ======================
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


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Đăng xuất thành công")
    return redirect("home")

@login_required
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        bai_viet = form.save(commit=False)
        bai_viet.TACGIA = request.user
        bai_viet.save()
        form.save_m2m()
        messages.success(request, "Đã đăng bài viết mới.")
        return redirect("post_detail", id=bai_viet.id)

    context = shared_context()
    context.update(
        {
            "form": form,
            "TIEU_DE_TRANG": "Thêm bài viết",
            "TEN_NUT": "Đăng bài",
        }
    )
    return render(request, "post_form.html", context)


@login_required
def post_update(request, id):
    bai_viet = get_object_or_404(POST, id=id)
    if not user_can_manage_post(request, bai_viet):
        messages.error(request, "Bạn chỉ có thể sửa bài viết do chính bài mình đăng.")
        return redirect("post_detail", id=bai_viet.id)

    form = PostForm(request.POST or None, request.FILES or None, instance=bai_viet)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Đã cập nhật bài viết.")
        return redirect("post_detail", id=bai_viet.id)

    context = shared_context()
    context.update(
        {
            "form": form,
            "BAIVIET": bai_viet,
            "TIEU_DE_TRANG": "Sửa bài viết",
            "TEN_NUT": "Lưu thay đổi",
        }
    )
    return render(request, "post_form.html", context)


@login_required
def post_delete(request, id):
    bai_viet = get_object_or_404(POST, id=id)
    if not user_can_manage_post(request, bai_viet):
        messages.error(request, "Bạn chỉ có thể xóa chính bài mình đăng.")
        return redirect("post_detail", id=bai_viet.id)

    if request.method == "POST":
        bai_viet.delete()
        messages.success(request, "Đã xóa bài viết.")
        return redirect("home")

    context = shared_context()
    context["BAIVIET"] = bai_viet
    return render(request, "post_confirm_delete.html", context)
