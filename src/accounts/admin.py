from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from .models import CustomUser

# from .forms import CustomAdminChangeForm

# class UserAdmin(BaseUserAdmin):
#     form = CustomAdminChangeForm

#     list_display = (
#         "email",
#         "active",
#         "staff",
#         "admin",
#     )
#     list_filter = (
#         "admin",
#         "active",
#     )
#     filter_horizontal = ()
#     ordering = ("email",)
#     search_fields = ('email',)

#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('プロフィール', {'fields': (
#             'username',
#             'department',
#             'phone_number',
#             'gender',
#             'birthday',
#         )}),
#         ('権限', {'fields': ('staff','admin',)}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2')}
#         ),
#     )

CustomUser = get_user_model()

admin.site.register(CustomUser)
# admin.site.register(User, UserAdmin)
#Profileクラスは不要になったのでコメントアウト
# admin.site.register(Profile)