from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Clothes,saved,experiment,history,feedback


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

class ExperimentSerializer(serializers.ModelSerializer):
    models_photo_path=serializers.ImageField(read_only=True)
    class Meta:
        model=experiment
        fields=['id','user_photo_path',"clothes_photo_path",'models_photo_path']

class FeedbackSerializer(serializers.ModelSerializer):
    experiment=ExperimentSerializer()
    def validate(self, data):

        
        if data['rate'] > 5 or data['rate'] < 0 :
            raise serializers.ValidationError({"rate": "invalid data"})
        return data
    class Meta:
        model=feedback
        fields=['id','rate','description','experiment']
    
class HistorySerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    experiment=ExperimentSerializer(read_only=True)
    class Meta:
        model=history
        fields=["id","user","experiment","Created_at"]
