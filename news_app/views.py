from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PostForm, CommentForm
from .models import CATEGORY, POST, COMMENT
from django.http import JsonResponse
import json

def shared_context(tu_khoa=""):
    return {
        "LIST_DANHMUC": CATEGORY.objects.all(),
        "TU_KHOA": tu_khoa,
    }

def user_can_manage_post(request, bai_viet):
    return request.user.is_authenticated and bai_viet.TACGIA_id == request.user.id


# ====================== HOME ======================
def home_view(request):
    TU_KHOA = request.GET.get('q', '')
    DANH_MUC_ID = request.GET.get('danh_muc', '') 

    LIST_DANHMUC = CATEGORY.objects.all()
    
    DANHSACH_BAIVIET = POST.objects.all().order_by('-NGAYDANG')

    #Lọc theo từ khóa tìm kiếm (nếu có)
    if TU_KHOA:
        DANHSACH_BAIVIET = DANHSACH_BAIVIET.filter(
            Q(TITLE__icontains=TU_KHOA) |
            Q(BAIVIET__NAME__icontains=TU_KHOA)
        )

    if DANH_MUC_ID:
        DANHSACH_BAIVIET = DANHSACH_BAIVIET.filter(BAIVIET_id=DANH_MUC_ID)

    return render(request, 'home.html', {
        'DANHSACH_BAIVIET': DANHSACH_BAIVIET,
        'TU_KHOA': TU_KHOA,
        'LIST_DANHMUC': LIST_DANHMUC,
    })


# ====================== CHI TIẾT + BÌNH LUẬN ======================
def post_detail(request, id):
    BAIVIET = get_object_or_404(POST, id=id)
    CO_THE_QUAN_LY = user_can_manage_post(request, BAIVIET)
    binh_luan = BAIVIET.comments.select_related('NGUOIBINHLUAN').order_by('-NGAYBINHLUAN')
    comment_form = CommentForm()

    return render(request, 'post_detail.html', {
        'BAIVIET': BAIVIET,
        'CO_THE_QUAN_LY': CO_THE_QUAN_LY,
        'binh_luan': binh_luan,
        'comment_form': comment_form,
    })


@login_required
def add_comment(request, id):
    BAIVIET = get_object_or_404(POST, id=id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.THONGTIN = BAIVIET
            comment.NGUOIBINHLUAN = request.user
            comment.save()
            messages.success(request, 'Bình luận của bạn đã được đăng.')
        else:
            messages.error(request, 'Bình luận không được để trống.')

    return redirect('post_detail', id=id)

@login_required
def delete_comment(request, id):
    comment = get_object_or_404(COMMENT, id=id)
    post_id = comment.THONGTIN.id

    if request.user == comment.NGUOIBINHLUAN or request.user.is_staff:
        comment.delete()
        messages.success(request, 'Đã xóa bình luận.')
    else:
        messages.error(request, 'Bạn không có quyền xóa bình luận này.')

    return redirect('post_detail', id=post_id)


# ====================== AUTH ======================
from .forms import RegisterForm


# ====================== REGISTER ======================
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
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
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return redirect('home')


# ====================== BÀI VIẾT ======================
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
    context.update({
        "form": form,
        "TIEU_DE_TRANG": "Thêm bài viết",
        "TEN_NUT": "Đăng bài",
    })
    return render(request, "post_form.html", context)


@login_required
def post_update(request, id):
    bai_viet = get_object_or_404(POST, id=id)
    if not user_can_manage_post(request, bai_viet):
        messages.error(request, "Bạn chỉ có thể sửa bài viết do chính mình đăng.")
        return redirect("post_detail", id=bai_viet.id)

    form = PostForm(request.POST or None, request.FILES or None, instance=bai_viet)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Đã cập nhật bài viết.")
        return redirect("post_detail", id=bai_viet.id)

    context = shared_context()
    context.update({
        "form": form,
        "BAIVIET": bai_viet,
        "TIEU_DE_TRANG": "Sửa bài viết",
        "TEN_NUT": "Lưu thay đổi",
    })
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

@login_required
def edit_comment(request, id):
    comment = get_object_or_404(COMMENT, id=id)

    if request.user != comment.NGUOIBINHLUAN:
        return JsonResponse({'success': False, 'error': 'Không có quyền sửa.'}, status=403)

    if request.method == 'POST':
        data = json.loads(request.body)
        noi_dung = data.get('noi_dung', '').strip()

        if not noi_dung:
            return JsonResponse({'success': False, 'error': 'Nội dung không được trống.'})

        comment.NOIDUNG = noi_dung
        comment.save()
        return JsonResponse({'success': True, 'noi_dung': comment.NOIDUNG})

    return JsonResponse({'success': False, 'error': 'Phương thức không hợp lệ.'}, status=405)