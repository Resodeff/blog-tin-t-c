from django.db import models
from django.contrib.auth.models import User

class CATEGORY(models.Model):
    NAME = models.CharField(max_length=100, verbose_name="Tên danh mục")

    def __str__(self):
        return self.NAME

class TAG(models.Model):
    NAME = models.CharField(max_length=50, verbose_name="Tên thẻ")

    def __str__(self):
        return self.NAME
    
class POST(models.Model):
    TITLE = models.CharField(max_length=200, verbose_name="Tiêu đề bài viết")
    CONTENT = models.TextField(verbose_name="Nội dung")

    TACGIA = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Tác giả")
    BAIVIET = models.ForeignKey(CATEGORY, on_delete=models.SET_NULL, null=True, verbose_name="Danh mục")
    THELOAI = models.ManyToManyField(TAG, blank=True, verbose_name="Thẻ")
    HINHANH = models.ImageField(upload_to="Image_file", blank=True, null=True, verbose_name="Hình ảnh blog")

    NGAYDANG = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    NGAYSUA = models.DateTimeField(auto_now=True, verbose_name="Ngày sỉnh sửa")

    def __str__(self):
        return self.TITLE
    
class COMMENT(models.Model):
    THONGTIN = models.ForeignKey(POST, related_name="comments", on_delete=models.CASCADE)

    NGUOIBINHLUAN = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người bình luận")
    NOIDUNG = models.TextField(verbose_name="Nội dung bình luận")
    NGAYBINHLUAN = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bình luận của {self.NGUOIBINHLUAN.username} trên bài '{self.THONGTIN.TITLE}'"
