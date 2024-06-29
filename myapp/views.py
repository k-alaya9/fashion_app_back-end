from rest_framework import viewsets
from .serializers import UserSerializer,ClothesSerializer,SavedSerializer
from django.contrib.auth.models import User
from .models import Clothes , saved
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
import json
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class ClothesViewSet(viewsets.ModelViewSet):
    queryset=Clothes.objects.all()
    serializer_class=ClothesSerializer
    permission_classes=[IsAuthenticated]

class SavedViewSet(viewsets.ModelViewSet):
    serializer_class=SavedSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        queryset =saved.objects.all()
        user = self.request.user
        queryset = queryset.filter(user=user)
        return queryset 
    def create(self, request, *args, **kwargs):
        data=json.loads(self.request.body)
        Clothes_id = data["cloth_id"]
        user = self.request.user
        try:
            clothes=Clothes.objects.get(id=Clothes_id)
            save = saved.objects.create(clothes=clothes, user=user)
            return Response(self.serializer_class(save).data, status=status.HTTP_201_CREATED)
        except Clothes.DoesNotExist: 
            return Response("Cloth_id is not found",status=status.HTTP_404_NOT_FOUND)