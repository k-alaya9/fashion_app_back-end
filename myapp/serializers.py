from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Clothes,saved


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ClothesSerializer(serializers.ModelSerializer):
    saved_id= serializers.SerializerMethodField(method_name='get_save')
    class Meta:
        model=Clothes
        fields=["id","name","description","image_url","saved_id"]
    def get_save(self, obj):
        request=self.context.get('request', None)
        user_id = request.user.id
        try:
            save = saved.objects.get(clothes=obj, user=user_id)
            return save.id
        except saved.DoesNotExist:
            return 0

class SavedSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    Clothes=ClothesSerializer(read_only=True)
    class Meta:
        model=saved
        fields=["id","user","Clothes","Created_at"]
