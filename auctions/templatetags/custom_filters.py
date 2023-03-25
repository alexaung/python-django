from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def get_username_or_full_name(user):
    if not user.first_name and not user.last_name:
        return user.username.upper()
    else:
        return f"{user.first_name.upper()} {user.last_name.upper()}"
