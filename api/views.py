from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import UserSerializer
from api.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('created_at')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
