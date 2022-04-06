from rest_framework import serializers
from .models import Tweet, Comment, Like
from users.models import User


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'author', 'tweet')


class CommentSerializer(serializers.ModelSerializer):
    # owner = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='user-detail')
    owner = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')

    comments = serializers.HyperlinkedIdentityField(view_name='api:comment-list')

    class Meta:
        # fields = ('id', 'text', 'owner', 'is_public', 'likes_count', 'comments_count', 'comments', 'parent',
        #           'created_at', 'modified_at')
        model = Comment

        fields = ('id', 'text', 'owner', 'likes_count',
                  'comments_count', 'comments', 'parent', 'created_at', 'modified_at')

    # def get_fields(self):
    #     fields = super(CommentSerializer, self).get_fields()
    #     fields['comments'] = CommentSerializer(many=True, read_only=True)
    #
    #     return fields


class TweetSerializer(serializers.ModelSerializer):
    # owner = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='user-detail')
    owner = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    comments = serializers.HyperlinkedIdentityField(view_name='api:comment-list')

    class Meta:
        model = Tweet
        fields = ('id', 'text', 'owner', 'likes_count', 'comments_count', 'comments',
                  'created_at', 'modified_at')
        read_only_fields = ('created_at', 'modified_at')

        # extra_kwargs = {
        #     'email': {'write_only': True},
        #     'password': {'write_only': True},
        # }


# class TweetCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tweet
#         fields = ('text', 'owner',)


class UserTweetsSerializer(serializers.ModelSerializer):
    tweets = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tweet.objects.all()
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'tweets')
