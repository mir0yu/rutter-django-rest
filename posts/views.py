from django.db.models import Q
from rest_framework import generics
from rest_framework.exceptions import NotAcceptable, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.models import Like, Comment, Tweet
from posts.serializers import LikeSerializer, CommentSerializer
from posts.utils import override_view_attributes
from posts.serializers import TweetSerializer

# from posts.serializers import TweetCreateSerializer


class CreateDeleteLikeView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        override_view_attributes(self)

    def perform_create(self, serializer):
        if self.request.data['author'] != str(self.request.user.id):
            raise NotAcceptable("Not authorized.")

        queryset = self.filter_queryset(self.get_queryset())
        subset = queryset.filter(Q(author_id=self.request.data['author']) & Q(tweet_id=self.request.data['tweet']))

        # If it's already liked, then just dislike.
        if subset.count() > 0:
            subset.first().delete()
            return

        serializer.save()


class CreateCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        override_view_attributes(self)

    def perform_create(self, serializer):
        parent_id = int(self.request.data['parent'])
        tweets = Tweet.objects.filter(id=parent_id, is_public=True)

        if tweets.count() != 1:
            raise NotFound()

        serializer.save(owner=self.request.user, type=1, is_public=True, parent_id=parent_id)


# class CreateTweetView(generics.CreateAPIView):
#     queryset = Tweet.objects.all()
#     serializer_class = TweetCreateSerializer


class ListTweetView(generics.ListCreateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        override_view_attributes(self)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, type=0, is_public=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter((Q(owner=request.user) | Q(is_public=True)) & Q(type=0))

        for tweet in queryset:
            tweet_id = tweet.id
            likes_count = Like.objects.filter(tweet=tweet_id).count()

            tweet.likes_count = likes_count
            tweet.comments_count = tweet.comments.all().count()
            tweet.save()

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ListPublicTweetsView(generics.ListAPIView):
    queryset = Tweet.objects.filter(is_public=True)
    serializer_class = TweetSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(Q(is_public=True) & Q(type=0))

        for tweet in queryset:
            tweet_id = tweet.id
            likes_count = Like.objects.filter(tweet=tweet_id).count()

            tweet.likes_count = likes_count
            tweet.comments_count = tweet.comments.all().count()
            tweet.save()

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ListUpdateDeleteCommentView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        override_view_attributes(self)

    def perform_update(self, serializer):
        comment_id = int(self.kwargs.get('pk'))

        queryset = self.filter_queryset(self.queryset)
        queryset = queryset.filter(Q(id=comment_id) & Q(owner=self.request.user))

        if queryset.count() != 1:
            raise NotFound("Comment not found.")

        comment = queryset.get()

        serializer.save(parent=comment.parent, is_public=True)


class ListUpdateDeleteTweetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        override_view_attributes(self)
