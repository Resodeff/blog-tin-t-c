from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import POST, COMMENT

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

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = COMMENT
        fields = ['NOIDUNG']
        widgets = {
            'NOIDUNG': forms.Textarea(attrs={
                'class': 'form-control rounded-3',
                'rows': 3,
                'placeholder': 'Viết bình luận của bạn...',
            }),
            
        }
        labels = {
            'NOIDUNG': ''
        }

