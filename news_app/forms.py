from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import POST


class PostForm(forms.ModelForm):
    class Meta:
        model = POST
        fields = ["TITLE", "CONTENT", "BAIVIET", "THELOAI", "HINHANH"]
        labels = {
            "TITLE": "Tiêu đề",
            "CONTENT": "Nội dung",
            "BAIVIET": "Danh mục",
            "THELOAI": "Thể loại",
            "HINHANH": "Hình ảnh",
        }
        widgets = {
            "TITLE": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập tiêu đề bài viết",
                }
            ),
            "CONTENT": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 8,
                    "placeholder": "Nhập nội dung bài viết",
                }
            ),
            "BAIVIET": forms.Select(attrs={"class": "form-select"}),
            "THELOAI": forms.SelectMultiple(attrs={"class": "form-select"}),
            "HINHANH": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class DangKyForm(UserCreationForm):
    username = forms.CharField(
        label="Ten dang nhap",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nhap ten dang nhap"}
        ),
    )
    password1 = forms.CharField(
        label="Mat khau",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Nhap mat khau"}
        ),
    )
    password2 = forms.CharField(
        label="Xac nhan mat khau",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Nhap lai mat khau"}
        ),
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class DangNhapForm(AuthenticationForm):
    username = forms.CharField(
        label="Ten dang nhap",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nhap ten dang nhap"}
        ),
    )
    password = forms.CharField(
        label="Mat khau",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Nhap mat khau"}
        ),
    )
