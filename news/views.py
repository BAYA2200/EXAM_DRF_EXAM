from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from news.models import News, Comment, Status, NewsStatus, CommentStatus
from news.permissions import NewsPermission, IsAdminUserPermission
from news.serializers import NewsSerializers, CommentSerializers, StatusSerializers, NewsStatusSerializers, \
    CommentStatusSerializers


class NewsListCreateAPIView(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializers
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    authentication_classes = [TokenAuthentication, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NewsRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializers
    permission_classes = [IsAuthenticatedOrReadOnly, NewsPermission]
    authentication_classes = [TokenAuthentication, ]


class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    authentication_classes = [TokenAuthentication, ]

    def perform_create(self, serializer):
        news_id = self.kwargs.get('pk')
        news = get_object_or_404(News, id=news_id)
        serializer.save(author=self.request.user, news=news)


class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = [IsAuthenticatedOrReadOnly, NewsPermission]
    authentication_classes = [TokenAuthentication, ]

    def perform_update(self, serializer):
        news_id = self.kwargs.get('news_id')
        comment_id = self.kwargs.get('pk')

        # Найти комментарий, который вы хотите обновить
        comment = get_object_or_404(Comment, id=comment_id, news_id=news_id)
        # Сохранить изменения в комментарии
        serializer.save(author=self.request.user, news_id=news_id, comment=comment)


class StatusListCreateAPIView(ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializers
    permission_classes = [IsAdminUserPermission, ]


class StatusRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializers
    permission_classes = [IsAdminUserPermission, ]



class NewsStatusCreateAPIView(CreateAPIView):
    queryset = NewsStatus.objects.all()
    serializer_class = NewsStatusSerializers
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def perform_create(self, serializer):
        author = self.request.user
        news_id = self.kwargs.get('news_id')
        slug = self.kwargs.get('slug')

        try:
            status_obj = Status.objects.get(name=slug)
        except Status.DoesNotExist:
            raise ValidationError({"error": "Статус не существует."}, code=status.HTTP_404_NOT_FOUND)

        serializer.save(status=status_obj, author=author, news_id=news_id)

class CommentStatusCreateAPIView(CreateAPIView):
    queryset = CommentStatus.objects.all()
    serializer_class = CommentStatusSerializers
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, news_id, comment_id, slug):
        # Get the comment
        comment = get_object_or_404(Comment, id=comment_id, news_id=news_id)

        # Get the authenticated user
        author = self.request.user

        # Check if the user has already added a status for this comment
        existing_status = CommentStatus.objects.filter(author=author, comment=comment).first()

        if existing_status:
            return Response({"error": "You already added status"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get or create the status
            status_obj, created = Status.objects.get_or_create(slug=slug, defaults={'name': slug})

            # Create the CommentStatus
            CommentStatus.objects.create(status=status_obj, author=author, comment=comment)

            return Response({"message": "Status added"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)