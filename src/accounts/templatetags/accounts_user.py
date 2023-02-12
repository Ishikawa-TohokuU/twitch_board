from django import template

register = template.Library()

@register.filter # デコレーター
def user_display(user):
    user_display = "ゲスト"
    if user.is_authenticated:
        user_display = user.username
    return user_display