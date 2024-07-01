from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Clothes(models.Model):
    name = models.CharField(max_length=100)
    description=models.TextField()
    image_url=models.ImageField(upload_to='media/image/',null=False,blank=False)

    def __str__(self):
        return self.name


class saved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE)
    Created_at= models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'clothes')

    def __str__(self):
        return f"{self.user.username}: {self.clothes.name}"


class experiment(models.Model):
    user_photo_path=models.ImageField(upload_to='media/user_photo/')
    clothes_photo_path=models.ImageField(upload_to="media/cloths_photo/")
    models_photo_path=models.ImageField(upload_to='media/model_photo')

    def __str__(self):
        return self.models_photo_path


class feedback(models.Model):
    experiment=models.ForeignKey(experiment,on_delete=models.CASCADE)
    rate=models.DecimalField(decimal_places=1,max_digits=1)
    description=models.TextField(null=True,blank=True)


class history(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    experiment=models.ForeignKey(experiment,on_delete=models.CASCADE)
    Created_at=models.DateField(auto_now_add=True)