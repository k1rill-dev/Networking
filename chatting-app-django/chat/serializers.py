from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']

# class ChatRoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChatRoom
#         fields = ['room_name', 'room_size','room_code', 'members']
#
#     def save(self, **kwargs):
#         room = ChatRoom(
#             room_name = self.validated_data['room_name'],
#             room_size = self.validated_data['room_size'],
#             room_code = get_unique_room_code(),
#         )
#         room.save()
#         print(self.validated_data['members'])
#         user = self.validated_data['members']
#         username = user[0].username
#         user = get_object_or_404(User, username=username)
#         room.members.add(user)
#         # room.save()
#         return room