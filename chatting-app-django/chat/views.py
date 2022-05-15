from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import time
from .models import Message, Profile
from .forms import SignUpForm
from .serializers import MessageSerializer, UserSerializer
from . import RSA


def index(request):
    if request.user.is_authenticated:
        return redirect('chats')
    if request.method == 'GET':
        return render(request, 'chat/index.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('{"error": "User does not exist"}')
        return redirect('chats')


def logout_user(request):
    logout(request)
    return redirect('index')


def user(request):
    return render(request, 'chat/lk.html', {})


class SearchResultsView(ListView):
    model = User
    template_name = 'chat/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = User.objects.filter(
            Q(name__icontains=query) | Q(state__icontains=query)
        )
        return object_list


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if request.method == 'GET':
        rsa = RSA.Rsa()
        aes = RSA.Aes()
        secret_key = Profile.objects.get(user=receiver)
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        # print(dir(messages))
        # print(type(messages))
        # messages.message = '234432342234432'
        for message in messages:
            message.message = aes.dec_aes(message.message, rsa.decript(secret_key.aes_key, secret_key.secret_key))
            message.save()

        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)

        serializer = MessageSerializer(messages, many=True, context={'request': request})
        print(serializer.data)

        messages1 = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        for i in messages1:
            i.is_read = True
            i.message = aes.enc_aes(i.message, rsa.decript(secret_key.aes_key, secret_key.secret_key))
            i.save()

        print(serializer.data)
        return JsonResponse(serializer.data, safe=False)


    elif request.method == 'POST':
        data = JSONParser().parse(request)
        user_id = User.objects.get(username=data['receiver'])
        open_key = Profile.objects.get(user=user_id.id)
        rsa = RSA.Rsa()
        aes = RSA.Aes()
        open_key.save()
        data['message'] = aes.enc_aes(data['message'], rsa.decript(open_key.aes_key, open_key.secret_key))
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def register_view(request):
    if request.method == 'POST':
        print("working1")
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            # print(user.id, 13241234424244234)
            # Profile.objects.filter(id=user.id).update(secret_key='ddd', open_key='3123')
            rsa = RSA.Rsa()
            key = Profile()
            key.secret_key = rsa.get_secret_key()
            key.open_key = rsa.get_open_key()
            aes = RSA.Aes()
            aes_key = aes.print_key()
            key_aes_enc = rsa.encript(aes_key, rsa.get_open_key())
            key.aes_key = key_aes_enc
            key.user = int(user.id)
            key.save()
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('chats')
    else:
        print("working2")
        form = SignUpForm()
    template = 'chat/register.html'
    context = {'form': form}
    return render(request, template, context)


def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chat/chat.html',
                      {'users': User.objects.exclude(username=request.user.username)})


def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        rsa = RSA.Rsa()
        aes = RSA.Aes()
        secret_key1 = Profile.objects.get(user=receiver)
        secret_key2 = Profile.objects.get(user=sender)
        key_aes1 = Profile.objects.get(user=receiver)
        key_aes2 = Profile.objects.get(user=sender)
        # aes.dec_aes(i.message, rsa.decript(key_aes1, secret_key1))
        list1 = [(aes.dec_aes(i.message, rsa.decript(key_aes1.aes_key, secret_key1.secret_key)), 1, i.timestamp) for i
                 in Message.objects.filter(sender_id=sender, receiver_id=receiver)]
        list2 = [(aes.dec_aes(i.message, rsa.decript(key_aes2.aes_key, secret_key2.secret_key)), 0, i.timestamp) for i
                 in Message.objects.filter(sender_id=receiver, receiver_id=sender)]
        a = sorted(list2 + list1, key=lambda x: x[-1])
        # qwerty = Message.objects.filter(sender_id=sender, receiver_id=receiver)
        return render(request, "chat/messages.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'receiver': User.objects.get(id=receiver),
                       'messages': a})

# class GetOrCreateRoomApi(APIView):
#
#     permission_classes = (IsAuthenticated,)
#
#     # get the rooms in which the user is enrolled
#     def get(self, request):
#         user = self.get_user(request)
#         rooms = user.chatroom_set.all()
#         serializer = ChatRoomSerializer(rooms, many=True)
#         # serializer.is_valid(raise_exception=True)
#         return Response(serializer.data)
#
#
#     def post(self, request):
#         serializer = ChatRoomSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
# class JoinRoomApi(APIView):
#
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request):
#         serializer = AddUserToRoomSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         res = serializer.save()
#         if res is None:
#             return Response({"error":"Can not Register You to Room"})
#         return Response(serializer.data)
