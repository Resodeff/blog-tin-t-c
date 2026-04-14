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


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    redirect_to = request.POST.get("next") or request.GET.get("next") or reverse("home")
    if not url_has_allowed_host_and_scheme(
        redirect_to,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        redirect_to = reverse("home")

    form = DangNhapForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        messages.success(request, "Dang nhap thanh cong.")
        return redirect(redirect_to)

    context = shared_context()
    context.update({"form": form, "next": redirect_to})
    return render(request, "registration/login.html", context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = DangKyForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Tao tai khoan thanh cong. Ban da duoc dang nhap.")
        return redirect("home")

    context = shared_context()
    context["form"] = form
    return render(request, "registration/register.html", context)


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Dang xuat thanh cong.")
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
