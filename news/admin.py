from django.contrib import admin

# Register your models here.
from news.models import News, Status, NewsStatus, CommentStatus

admin.site.register(News)
admin.site.register(Status)
admin.site.register(NewsStatus)
admin.site.register(CommentStatus)


