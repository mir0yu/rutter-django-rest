from rest_framework import generics
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer

from posts.permissions import IsOwner


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    lookup_field = 'username'


class SelfUserView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner]

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(User, pk=request.user.pk)
        serializer = self.get_serializer(instance, many=False)
        return Response(serializer.data)

#
# class UserDetailsView(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
