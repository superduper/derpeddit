from django.shortcuts import get_object_or_404
from rest_framework import generics, authentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from posts.models import Post, Comment
from posts.serializers import VoteSerializer, PostCreateSerializer, PostSerializer, CommentSerializer, PostDetailedSerializer


class PostListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    model = Post

    def get_queryset(self):
        mode = self.request.GET.get("mode", "top")
        if mode =="newest":
            return Post.objects.all().order_by('-created')
        else:
            return Post.objects.all()

    def get_serializer(self, instance=None, data=None, files=None, many=False, partial=False):
        if not instance:
            # manual owner resultion
            if data:
                new_data = dict(data, owner=self.request.user.pk)
            else:
                new_data = data
            return PostCreateSerializer(instance, new_data, files, many, partial)
        return PostSerializer(instance, data, files, many, partial)

    def pre_save(self, obj):
        obj.owner = self.request.user

class CommentListView(generics.ListCreateAPIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["pk"])

    def pre_save(self, obj):
        obj.owner = self.request.user

    def get_serializer(self, instance=None, data=None, files=None, many=False, partial=False):
        if not instance:
            # manual owner resultion
            if data:
                instance = Comment(owner=self.request.user)
                new_data = dict(data, post=self.kwargs["pk"])
            else:
                new_data = data
            return CommentSerializer(instance, new_data, files, many, partial)
        return CommentSerializer(instance, data, files, many, partial)

class PostView(generics.RetrieveUpdateDestroyAPIView):
    model = Post
    serializer_class = PostDetailedSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )

class VoteView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = VoteSerializer(data=request.DATA)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)
        positive = serializer.data.get("positive")
        negative = serializer.data.get("negative")
        post.submit_vote(request.user, positive, negative)
        return Response(dict(new_post_score=post.score))
