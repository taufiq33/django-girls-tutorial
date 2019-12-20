from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField("Judul",max_length=200)
    text = models.TextField("Isi")
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    @property
    def is_long_title(self):
        return len(self.title) > 10

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name="comments")
    author = models.CharField("Nama", max_length=200)
    text = models.TextField("Isi Komentar")
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve_comment(self):
        self.approve_comment = True
        self.save()

    class Meta():
        ordering = ['created_date']

    def __str__(self):
        return self.text