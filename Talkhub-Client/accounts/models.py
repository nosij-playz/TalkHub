from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, userid, name, email, password=None):
        if not userid:
            raise ValueError("User must have a UserID")
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(userid=userid, name=name, email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, userid, name, email, password=None):
        user = self.create_user(userid, name, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
    
class History(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.userid} → {self.receiver.userid} at {self.timestamp}"
    
class Online(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    relay_id = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return f"{self.user.userid} ({self.relay_id})"
    
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    userid = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'userid'
    REQUIRED_FIELDS = ['name', 'email']

    def __str__(self):
        return self.userid

