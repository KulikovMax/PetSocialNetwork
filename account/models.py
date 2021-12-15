from datetime import datetime, timedelta

import jwt
import django.utils.timezone
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        if password is None:
            raise TypeError('User must have a password.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)

    email = models.EmailField(db_index=True, unique=True)

    first_name = models.CharField(default='', max_length=255, editable=True)
    last_name = models.CharField(default='', max_length=255, editable=True)

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    last_login = models.DateTimeField(blank=True, default=timezone.now)
    last_request = models.DateTimeField(blank=True, default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def update_last_login(self):
        self.last_login = django.utils.timezone.now()
        self.last_request = django.utils.timezone.now()
        self.save()

    def update_last_request(self):
        self.last_request = django.utils.timezone.now()
        self.save()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%S'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


class UserFollowing(models.Model):
    user = models.ForeignKey(User, related_name="following", on_delete=models.PROTECT)

    following_user = models.ForeignKey(User, related_name="followers", on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'following_user'], name="unique_followers")
        ]

    def __str__(self):
        return f'{self.user}, {self.following_user}'

    def return_user(self):
        return self.user

    def return_following_user(self):
        return self.following_user


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
