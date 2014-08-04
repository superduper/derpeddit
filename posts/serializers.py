from rest_framework import serializers
from core.serializers import ProfileSerializer
from posts.models import Post, Vote, Comment
from posts.serializers_fields import SubDocumentRelatedField, SubDocumentField


class PostCreateSerializer(serializers.ModelSerializer):
    """
    Used only when new post is created
    """
    class Meta:
        model = Post
        fields = ('title', 'text', 'link')


class CommentSerializer(serializers.ModelSerializer):
    """
    Read-only comment serialization
    """
    class Meta:
        model = Comment
    owner = SubDocumentField(serializer=ProfileSerializer)


class PostSerializer(serializers.ModelSerializer):
    """
    Read-only post serialization
    """
    class Meta:
        model = Post
    owner = SubDocumentField(serializer=ProfileSerializer)
    comments_total = serializers.SerializerMethodField("get_comments_total")

    def get_comments_total(self, instance):
        return instance.comments.count()


class PostDetailedSerializer(PostSerializer):
    """
    Post serialization with comments
    """
    comments = SubDocumentRelatedField(field="comments", serializer=CommentSerializer, many=True)


class VoteSerializer(serializers.Serializer):
    """
    Vote request parameter serializer
    """
    positive = serializers.BooleanField(required=False)
    negative = serializers.BooleanField(required=False)

    def validate(self, attrs):
        negative = attrs.get("negative")
        positive = attrs.get("positive")
        try:
            Vote.validate_vote_params(positive, negative)
        except ValueError:
            raise serializers.ValidationError("Either positive or negative should be set")
        return attrs
