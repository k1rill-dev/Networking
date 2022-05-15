from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.IntegerField(blank=True)
    open_key = models.CharField(max_length=100, blank=True)
    secret_key = models.CharField(max_length=100, blank=True)
    aes_key = models.CharField(max_length=100, blank=True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)

# class ChatRoom(models.Model):
#     room_name = models.CharField(max_length = 30)
#     room_size = models.IntegerField(default=5)
#     room_code = models.CharField(max_length=5)
#     members = models.ManyToManyField(User)
#     creation_date = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f'{self.pk}-{self.room_name}'
