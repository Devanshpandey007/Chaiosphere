from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not email:
            raise ValueError("Email can not be empty")
        user  = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user
        
class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username


class ChaiShop(models.Model):
    shop_name = models.CharField(max_length=255)
    adress = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    
class ChaiCategory(models.Model):
    product_name = models.CharField(max_length=255)
    chai_shop = models.ForeignKey(ChaiShop, on_delete = models.CASCADE)
