from django.conf import settings
from django.db import models
from django.utils import timezone
from django_quill.fields import QuillField


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=False)
    title = models.CharField(max_length=200)
    text = QuillField()
    is_edited = models.BooleanField(default=False, editable=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    likes = models.IntegerField(default=0, editable=True)

    def publish(self):
        self.created_at = timezone.now()
        self.save()

    def get_users_liked(self):
        query_set = Like.objects.all().filter(post=self.id)
        print(query_set)
        users_set = [x.user for x in query_set]
        print(users_set)
        return users_set

    def __str__(self):
        return self.title


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateField(default=timezone.now, editable=False)
