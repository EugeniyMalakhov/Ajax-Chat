from django.contrib import admin
from django.contrib.auth.models import User
from myapp.models import Message

admin.site.register(Message)
