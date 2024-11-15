from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# from django.contrib.auth.models import User
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm


# Create your views here.


def loginP(request):
    page = 'loginP'
    if request.user.is_authenticated:
        return redirect('homePage')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "user does not exist")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('homePage')
        else:
            messages.error(request, "email does not exist")

    context = {'page': page}
    return render(request, 'studentHive/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('homePage')


def registerUser(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('homePage')
        else:
            messages.error(request, "An error occurred during registration")

    return render(request, 'studentHive/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ' '

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    if q.strip() == '':
        room_messages = Message.objects.all()
    else:
        room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'studentHive/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('roomPage', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'studentHive/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user,
               'rooms': rooms,
               'room_messages': room_messages,
               'topics': topics}
    return render(request, 'studentHive/profile.html', context)


@login_required(login_url='loginP')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),

        )
        return redirect('homePage')

    context = {'form': form, 'topics': topics}
    return render(request, 'studentHive/room_form.html', context)


@login_required(login_url='loginP')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("You are not allowed here...")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('homePage')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'studentHive/room_form.html', context)


@login_required(login_url='loginP')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here...")

    if request.method == 'POST':
        room.delete()
        return redirect('homePage')
    return render(request, 'studentHive/delete.html', {'obj': room})


@login_required(login_url='loginP')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed here...")

    if request.method == 'POST':
        message.delete()
        return redirect('homePage')
    return render(request, 'studentHive/delete.html', {'obj': message})


@login_required(login_url='loginP')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    # user_form = UserForm(request.POST or None, instance=user)
    # profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('st-profile', pk=user.id)

    return render(request, 'studentHive/update_user.html', {'form': form})


def topicsPages(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ' '
    ttopics = Topic.objects.filter(name__icontains=q)
    return render(request, 'studentHive/topics.html', {'ttopics': ttopics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'studentHive/activity.html', {'room_messages': room_messages})
