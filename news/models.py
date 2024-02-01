from django.db import models

# Create your models here.
from django.db.models import Count

from account.models import Author


class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} and {self.author}"

class Comment(models.Model):
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    def get_status(self):
        statuses = CommentStatus.objects.filter(comment=self).values('status__name').annotate(count=Count('status'))

        result = {}

        for i in statuses:
            result[i['status__name']] = i['count']

        return result

class Status(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.slug} and {self.name}"


class NewsStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.OneToOneField(Status, on_delete=models.CASCADE)
    author = models.OneToOneField(Author, on_delete=models.CASCADE, unique=True)
    news = models.OneToOneField(News, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f"{self.status} and {self.author} and {self.news}"

class CommentStatus(models.Model):
    status = models.OneToOneField(Status, on_delete=models.CASCADE)
    author = models.OneToOneField(Author, on_delete=models.CASCADE, unique=True)
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f"{self.status} and {self.author} and {self.comment}"
