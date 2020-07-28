import bcrypt
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, nickname, password=None):
        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            nickname=nickname,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()

    email = models.EmailField(
        max_length=250,
        unique=True,
    )
    nickname = models.CharField(
        max_length=100,
        unique=True,
    )
    phone_number = models.CharField(
        max_length=14,
        default="",
        blank=True,
    )
    membership = models.CharField(
        max_length=5,
        default="",
        blank=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'  # email을 id로 사용합니다.
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['date_joined']

    def __str__(self):
        return "<%d %s>" % (self.pk, self.email)

    def set_password(self, raw_password):
        hashed_password = bcrypt.hashpw(
            raw_password.encode('utf-8'),  bcrypt.gensalt())
        self.password = hashed_password

    def check_password(self, hashed_password, input_password):
        if bcrypt.checkpw(input_password.encode('utf-8'), hashed_password):
            return True
        else:
            return False
