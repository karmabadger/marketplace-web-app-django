# chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'chat/chat.html', {})

@login_required
def room(request, room_name):
    context = {
        'room_name': room_name,
        'username': request.user.username,
        "user_id": request.user.id,
    }
    return render(request, 'chat/room.html', context)