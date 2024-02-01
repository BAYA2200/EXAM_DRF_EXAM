from rest_framework import serializers

from news.models import News, Comment, Status, NewsStatus, CommentStatus


class NewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'created', 'updated', 'author']


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class StatusSerializers(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class NewsStatusSerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsStatus
        fields = ['status', 'author', 'news']
        # добавим уникальность для комбинации полей
        unique_together = ['status', 'news', 'author']


class CommentStatusSerializers(serializers.ModelSerializer):
    class Meta:
        model = CommentStatus
        fields = "__all__"
        unique_together = ('status', 'author', 'comment')
