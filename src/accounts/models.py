from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.db.models.signals import pre_save, post_save
from allauth.account.signals import user_logged_in
from django.dispatch import receiver

# GENDER_CHOICE = [(None, "--"), ("m", "男性"), ("f", "女性")]

# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None):
#         if not email:
#             raise ValueError('Users must have an email address')

#         user = self.model(
#             email=self.normalize_email(email),
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_staffuser(self, email, password):
#         user = self.create_user(
#             email,
#             password=password,
#         )
#         user.staff = True
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password):
#         user = self.create_user(
#             email,
#             password=password,
#         )
#         user.staff = True
#         user.admin = True
#         user.save(using=self._db)
#         return user

# class User(AbstractBaseUser): # AbstractBaseUser: 'id', 'password', 'last_login'は備わっている
#     email = models.EmailField(
#         verbose_name='Eメールアドレス',
#         max_length=255,
#         unique=True,
#     )
#     active = models.BooleanField(default=True)
#     staff = models.BooleanField(default=False) 
#     admin = models.BooleanField(default=False)

#     objects = UserManager()

#     USERNAME_FIELD = 'email' # emailでログインできるようにする

#     def __str__(self):             
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return self.admin

#     def has_module_perms(self, app_label):
#         return self.admin

#     @property
#     def is_staff(self):
#         return self.staff

#     @property
#     def is_admin(self):
#         return self.admin

#     @property
#     def is_active(self):
#         return self.active
    
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     username = models.CharField(max_length=100, verbose_name="ユーザー名")
#     print(user)
#     department = models.CharField(max_length=100, blank=True, null=True, verbose_name="部署")
#     phone_number = models.IntegerField(blank=True, null=True, verbose_name="携帯番号")
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICE, default=None, verbose_name="性別", blank=True, null=True)
#     birthday = models.DateField(blank=True, null=True, verbose_name="生年月日")

#     def __str__(self):
#         return self.username

# import requests

class CustomUser(AbstractUser):
    # first_name = None
    def get_id(self):
        """Return the id for the user."""
        return self.id

@receiver(user_logged_in)
def username_firstname(request, user, **kwargs):
    if user.username != user.first_name:
        user_obj = CustomUser.objects.get(id=user.id)
        print("email =", user_obj.email)
        print('user_obj = ', user_obj)
        user_obj.username = user.first_name
        # user_obj.username = user.email
        user_obj.save()

