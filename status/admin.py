from django.contrib import admin
from .models import Status, Comment, CommentNotification


# Register your models here.
admin.site.register(Status)
admin.site.register(Comment)
admin.site.register(CommentNotification)