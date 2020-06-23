from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, 
                               related_name="posts")
    group = models.ForeignKey("Group", models.SET_NULL, blank=True, 
                               null=True, related_name="posts")

    class Meta:
        ordering = ["-pub_date"] 

    def __str__(self):   
        return f"{self.pub_date} {self.author} {self.text}"   


class Group(models.Model):
    title = models.CharField(max_length=200) 
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(max_length=200)

    def __str__(self):   
        return f"{self.title}"
