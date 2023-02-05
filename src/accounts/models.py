from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
import uuid

GENDER_CHOICE = [(None, "--"), ("m", "男性"), ("f", "女性")]

class UserManager(BaseUserManager):
    # def create_user(self, email, password=None):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an email address')

        user = self.model(
            # email=self.normalize_email(email),
            username=self.username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_staffuser(self, username, email, password):
    def create_staffuser(self, username, password):
        user = self.create_user(
            username, # add
            # email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    # def create_superuser(self, username, email, password):
    def create_superuser(self, username, password):
        user = self.create_user(
            username, # add
            # email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser): # AbstractBaseUser: 'id', 'password', 'last_login'は備わっている
    email = models.EmailField(
        verbose_name='Eメールアドレス',
        max_length=255,
        # unique=True,
        default=False,
    )
    username = models.CharField(unique=True, max_length=100, default=uuid.uuid1, verbose_name="ユーザー名")
    USERNAME_FIELD = 'username'
    # USERNAME_FIELD = 'email' # emailでログインできるようにする

    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) 
    admin = models.BooleanField(default=False)

    objects = UserManager()


    def __str__(self):      
        # return self.email       
        return self.username

    def has_perm(self, perm, obj=None):
        return self.admin

    def has_module_perms(self, app_label):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # username = models.CharField(max_length=100, verbose_name="ユーザー名")
    print(user)
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name="部署")
    phone_number = models.IntegerField(blank=True, null=True, verbose_name="携帯番号")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, default=None, verbose_name="性別", blank=True, null=True)
    birthday = models.DateField(blank=True, null=True, verbose_name="生年月日")

    def __str__(self):
        return self.username


def post_user_created(sender, instance, created, **kwargs):
    if created:
        profile_obj = Profile(user=instance)
        # profile_obj.username = instance.email
        profile_obj.username = instance.username
        profile_obj.save()

post_save.connect(post_user_created, sender=User)