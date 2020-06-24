from django.test import TestCase, Client
from .models import Post, Group, User
from django.urls import reverse


class ProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.non_auth_user = Client()
        self.user = User.objects.create_user(username="test_user", 
                                             email="tstusr@test.ru", 
                                             password="12345")
        self.client.force_login(self.user)                                                                       
        self.group = Group.objects.create(title="test_group", slug="test_slug")
        self.client.post(reverse("new_post"),
        data={"group": "1", 'text': "New_post_test"}, follow=True)
        self.urls = [
        reverse("index"), 
        reverse("profile", kwargs={ "username": "test_user"}),
        reverse("post_view", kwargs={ "username": "test_user", "post_id": "1"}),
        reverse("group", kwargs={ "slug": "test_slug"})
        ]

    def check_post_in_page(self, url, text):
        response = self.client.get(url)
        return self.assertContains(response, text)         


    def test_profile(self):
        response = self.client.get(reverse("profile", kwargs={
                                           "username": 'test_user'}))
        self.assertEqual(response.status_code, 200)

    def new_post_test(self):
        response = self.client.get(reverse("new_post"))
        self.assertEqual(response.status_code, 200)
        response = self.non_auth_user.get(reverse("new_post"), follow=True)
        self.assertRedirects(response, "/auth/login/?next=/new/", 
                             status_code=302, target_status_code=200)       

    def post_test(self):
        for url in self.urls:
            self.check_post_in_page(url, "New_post_test")
        post = Post.objects.get(text="New_post_test")
        self.assertEqual(post.author.username, "test_user")
        quan = self.user.posts.all().count()
        self.assertEqual(quan, 1)
        self.assertEqual(post.group.id, 1)

    def post_edit_test(self): 
        for url in self.urls:
            response = self.client.get(url)
            self.assertNotContains (response, "post_edited")       
        self.client.post(reverse("post_edit", kwargs={
                'username': self.user.username, 'post_id': "1"}),
                data={'group': "1", 'text': "post_edited"}, follow=True)
        for url in self.urls:
            self.check_post_in_page(url, "post_edited")  

    
class CrashTest(TestCase):
    def setUp(self):
        self.client = Client()
              
    def test_code_404(self):
        response = self.client.get("/test_code_404/")
        self.assertEqual(response.status_code, 404)

class ImageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test_user", 
                                             email="tstusr@test.ru", 
                                             password="12345")
        self.client.force_login(self.user)                                                                       
        self.group = Group.objects.create(title="test_group", slug="test_slug")
        self.img = open("media/posts/test_image.jpeg", "rb")
        self.img_post = self.client.post(reverse("new_post"),
        data={"group": "1", 'text': "post_with_image_test", "image": self.img}, follow=True) 
        self.urls = [
        reverse("index"), 
        reverse("profile", kwargs={ "username": "test_user"}),
        reverse("post_view", kwargs={ "username": "test_user", "post_id": "1"}),
        reverse("group", kwargs={ "slug": "test_slug"})
        ]

    def image_test(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertContains(response, "<img class=")
            self.assertContains(response, "post_with_image_test") 

    def not_image_test(self):
        self.img = open("media/posts/not_image_file.txt", "rb")
        response = self.client.post(reverse("new_post"),
        data={
              "group": "1", 'text': "post_with_not_image_test", 
              "image": self.img
        }, follow=True)
        self.assertFormError(response, "form", "image", 
            "Загрузите правильное изображение. Файл, ко"\
            "торый вы загрузили, поврежден или не является изображением.")