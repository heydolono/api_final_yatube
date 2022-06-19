from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters, permissions
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Comment, Group, Post, Follow, User
from .mixins import CreateListViewSet
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    GroupSerializer,
    PostSerializer,
    FollowSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def create(self, serializer):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, serializer, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, serializer, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        get_object_or_404(Post, pk=post_id)
        new_queryset = Comment.objects.filter(post=post_id)
        return new_queryset

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get("post_id"))

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post_id=post_id)


class FollowViewSet(CreateListViewSet):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (permissions.IsAuthenticated,)
    search_fields = ("user__username", "following__username")

    def get_queryset(self):
        queryset = Follow.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        following = get_object_or_404(
            User, username=self.request.data["following"]
        )
        serializer.save(user=self.request.user, following=following)
