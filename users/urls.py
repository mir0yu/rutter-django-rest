from django.urls import path
from rest_framework import routers

from users.views import UserViewSet

from users.views import SelfUserView

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('users/me/', SelfUserView.as_view(), name='retrieve-user'),
]

urlpatterns += router.urls
