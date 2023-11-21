from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE,) # connect to the built-in django User model
    
    # additional fields
    portfolio_site = models.URLField(blank=True) # blank=True means that the field is not mandatory
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True)
    
    def __str__(self):
        return self.user.username