from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,**kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class UserProfile(models.Model):  
    user = models.OneToOneField(User, unique=True,on_delete = models.CASCADE)
    profile_picture = models.ImageField(upload_to='thumbpath', blank=True)


class History(models.Model):
        hist_id=models.AutoField(primary_key=True)
        user=models.ForeignKey(User,on_delete=models.CASCADE)
        deja_id=models.CharField(max_length=10000000,default="")
                    