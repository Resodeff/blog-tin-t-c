from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import CATEGORY, POST

class PostPermissionTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="pass123456")
        self.other_user = User.objects.create_user(
            username="other_user", password="pass123456"
        )
        self.category = CATEGORY.objects.create(NAME="Cong nghe")
        self.post = POST.objects.create(
            TITLE="Bai viet goc",
            CONTENT="Noi dung ban dau",
            TACGIA=self.owner,
            BAIVIET=self.category,
        )

    def test_logged_in_user_can_create_post(self):
        self.client.login(username="owner", password="pass123456")

        response = self.client.post(
            reverse("post_create"),
            {
                "TITLE": "Bài viết mới",
                "CONTENT": "Nội dung mới",
                "BAIVIET": self.category.id,
            },
        )

        bai_viet_moi = POST.objects.get(TITLE="Bài viết mới")
        self.assertRedirects(response, reverse("post_detail", args=[bai_viet_moi.id]))
        self.assertEqual(bai_viet_moi.TACGIA, self.owner)

    def test_owner_can_update_post(self):
        self.client.login(username="owner", password="pass123456")

        response = self.client.post(
            reverse("post_update", args=[self.post.id]),
            {
                "TITLE": "Bài viết đã sửa",
                "CONTENT": "Nội dung đã sửa",
                "BAIVIET": self.category.id,
            },
        )

        self.post.refresh_from_db()
        self.assertRedirects(response, reverse("post_detail", args=[self.post.id]))
        self.assertEqual(self.post.TITLE, "Bài viết đã sửa")

    def test_other_user_cannot_update_post(self):
        self.client.login(username="other_user", password="pass123456")

        response = self.client.post(
            reverse("post_update", args=[self.post.id]),
            {
                "TITLE": "Co gang sua trai phep",
                "CONTENT": "Noi dung khong hop le",
                "BAIVIET": self.category.id,
            },
            follow=True,
        )

        self.post.refresh_from_db()
        self.assertRedirects(response, reverse("post_detail", args=[self.post.id]))
        self.assertEqual(self.post.TITLE, "Bai viet goc")
        self.assertContains(
            response,
            "Ban chi co the sua bai viet do chinh minh dang.",
        )

    def test_owner_can_delete_post(self):
        self.client.login(username="owner", password="pass123456")

        response = self.client.post(reverse("post_delete", args=[self.post.id]))

        self.assertRedirects(response, reverse("home"))
        self.assertFalse(POST.objects.filter(id=self.post.id).exists())

    def test_other_user_cannot_delete_post(self):
        self.client.login(username="other_user", password="pass123456")

        response = self.client.post(
            reverse("post_delete", args=[self.post.id]),
            follow=True,
        )

        self.assertRedirects(response, reverse("post_detail", args=[self.post.id]))
        self.assertTrue(POST.objects.filter(id=self.post.id).exists())
        self.assertContains(
            response,
            "Ban chi co the xoa bai viet do chinh minh dang.",
        )
