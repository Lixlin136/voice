from django.db import models

# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
import random
from django.conf import settings


def user_avatar_path(instance, filename):
    # 头像保存路径: avatars/user_id/filename

    return f'avatars/{instance.id}/{filename}'



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)

    # 新增字段
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    signature = models.CharField(max_length=200, blank=True, null=True)

    def generate_verification_code(self):
        return str(random.randint(1000, 9999))

    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        print(self.avatar)
        return '/static/images/default_avatar.jpg'  # 默认头像路径

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # 添加 related_name 参数
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_user_permissions',  # 添加 related_name 参数
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class VerificationCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return (timezone.now() - self.created_at).total_seconds() < 300  # 5分钟有效
