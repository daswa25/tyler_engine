from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, security_code=0, verify_email=0,gender=None):
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_joined=timezone.now(),
            status=0,
            gender=gender,
            security_code=security_code,
            verify_email=verify_email,
            alive=0
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.status = 1
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=35)
    date_joined = models.DateTimeField(default=timezone.now)
    security_code = models.IntegerField(default=0)
    gender=models.CharField(max_length=50,null=True)
    verify_email = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    alive = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
class blog(models.Model):
    blog_title = models.CharField(max_length=100)
    blog_content = models.TextField(max_length=255)
    blog_slug = models.SlugField(max_length=100, default="", null=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_edited = models.DateTimeField(blank=True,null=True)
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.blog_slug:
            self.blog_slug = slugify(self.blog_title)
        
        super().save(*args, **kwargs)
class messages(models.Model):
        pid=models.IntegerField()
        fid=models.ForeignKey('User',on_delete=models.CASCADE)
        date_messaged=models.DateTimeField(default=timezone.now)
        last_date_messaged=models.DateTimeField(blank=True,null=True)
        read=models.IntegerField(default=0)
        message=models.CharField(max_length=255)
        
