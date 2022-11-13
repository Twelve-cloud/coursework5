from user.serializers import BasicUserSerializer
from user.serializers import FullUserSerializer
from rest_framework import viewsets
from user.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return FullUserSerializer
        return BasicUserSerializer
