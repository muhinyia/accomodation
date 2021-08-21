from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from .models import Room
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import auth, messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from landlord.models import Landlord, Inquiry

# homepage view


def index(request):
    return render(request, 'pages/index.html')


# view to display all rooms
def rooms(request):
    rooms = Room.objects.order_by('rent').filter(
        is_available=True, is_approved=True)
    # creating a paginator for rooms
    paginator = Paginator(rooms, 10)
    page = request.GET.get('page')
    paged_rooms = paginator.get_page(page)
    context = {'rooms': paged_rooms}
    return render(request, 'pages/rooms.html', context)


# single room view
def room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    context = {
        'room': room
    }
    return render(request, 'pages/room.html', context)


# Class Based View to create a room
class RoomCreateView(CreateView):
    model = Room
    template_name = 'landlord/room_form.html'
    fields = ['title', 'address', 'rent',
              'bond_amount', 'description', 'size', 'photo_main', 'photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5', ]
    success_url = reverse_lazy('accounts:landlord_dashboard')

# Class Based View to edit a room


class RoomEditView(UpdateView):
    model = Room
    template_name = 'landlord/form.html'

    fields = ['title', 'address', 'rent',
              'bond_amount', 'description', 'size', 'photo_main', 'is_available']
    success_url = reverse_lazy('accounts:landlord_dashboard')


# Class Based View to delete a room
class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'landlord/room_delete.html'
    success_url = reverse_lazy('accounts:landlord_dashboard')


# view to add a room
def add_room(request):
    if request.method == 'POST':
        title = request.POST['title']
        address = request.POST['address']
        rent = request.POST['rent']
        bond_amount = request.POST['bond']
        size = request.POST['size']
        description = request.POST['description']
        photo_main = request.FILES['photo_main']
        #photo_1 = request.FILES['photo_1']
        #photo_2 = request.FILES['photo_2']
        #photo_3 = request.FILES['photo_3']
        # get the landlord
        user = request.user
        this_user = get_object_or_404(User, username=user)
        this_landlord = get_object_or_404(Landlord, user=this_user)
        this_room = Room.objects.create(
            landlord=this_landlord, title=title, address=address, rent=rent, size=size, bond_amount=bond_amount, description=description, photo_main=photo_main, status='under review', is_available=True)  # for now set is_hired to True but remember to change it later for admin control
        this_room.save()
        messages.success(
            request, 'Room added successfully')
        return redirect('accounts:landlord_dashboard')
    return render(request, 'landlord/room_form.html')


# Create your views here.
def inquiry(request):
    if request.method == 'POST':
        room_id = request.POST['room_id']
        room = request.POST['room']
        email = request.POST['email']
        message = request.POST['message']
        user_id = request.POST['user_id']
        landlord_email = request.POST['landlord_email']
        # check if user has inquiry on this property already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Inquiry.objects.all().filter(
                room_id=room_id, user_id=user_id)
            if has_contacted:
                messages.error(
                    request, 'You have already made an inquiry for this room')
                return redirect('apartments:rooms')
        contacts = Inquiry(room=room, room_id=room_id,  email=email,  message=message,
                           user_id=user_id)
        contacts.save()
        # sending Email to Landlord
        send_mail(
            'Room Inquiry',
            'There has been an inquiry for ' + room +
            '.Please sign into the Your Dashboard for more information.',
            'YOUUR EMAIL HERE',
            [landlord_email, 'YOUR EMAIL HERE'],
            fail_silently=False
        )
        messages.success(
            request, 'Your request has been submitted successfully, Landlord will get back to you soon')
    return redirect('apartments:rooms')
