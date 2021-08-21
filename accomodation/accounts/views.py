from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from student.models import Student
from landlord.models import Landlord, Inquiry
from apartments.models import Room

# view to registering students


def student_register(request):
    if request.method == 'POST':
        # Get form Values
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # check if passwords match
        if password == password2:
            # check username whether the email exists in the system
            if User.objects.filter(username=email).exists():
                messages.error(request, 'A user with Email Exists!!')
                return redirect('accounts:register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email Exists!!!')
                    return redirect('accounts:register')
                else:
                    # adding user since all the validation passed
                    user = User.objects.create_user(
                        username=email, password=password, email=email)
                    user.save()
                    this_user = User.objects.get(username=email)

                    this_student = Student.objects.create(
                        user=this_user)
                    this_student.save()
                    messages.success(
                        request, 'You Have Registered Successfully')
                    return redirect('accounts:student_login')

        else:
            messages.error(request, 'Passwords must Match!!')
            return redirect('accounts:student_register')
    else:
        return render(request, 'student/register.html', )

# view for registering landlords


def landlord_register(request):
    if request.method == 'POST':
        # Get form Values
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # check if passwords match
        if password == password2:
            # check username whether the email exists in the system
            if User.objects.filter(username=email).exists():
                messages.error(request, 'A user with Email Exists!!')
                return redirect('accounts:register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email Exists!!!')
                    return redirect('accounts:register')
                else:
                    # adding user since all the validation passed
                    user = User.objects.create_user(
                        username=email, password=password, email=email)
                    user.save()
                    this_user = User.objects.get(username=email)

                    this_landlord = Landlord.objects.create(
                        user=this_user)
                    this_landlord.save()
                    messages.success(
                        request, 'You Have Registered Successfully')
                    return redirect('accounts:landlord_login')

        else:
            messages.error(request, 'Passwords must Match!!')
            return redirect('accounts:landlord_register')
    else:
        return render(request, 'landlord/register.html', )


def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are Logged in Welcome ')
            return redirect('apartments:rooms')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('accounts:student_login')
    return render(request, 'student/login.html')


def landlord_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are Logged in Welcome ')
            return redirect('accounts:landlord_dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('accounts:landlord_login')
    return render(request, 'landlord/login.html')


def moderator_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are Logged in Welcome ')
            return redirect('accounts:moderator_dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('accounts:moderator_login')
    return render(request, 'moderator/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are Logged out')

    return redirect('apartments:index')


def register(request):
    return render(request, 'pages/select_register.html')


def dashboard(request):
    user = request.user
    this_user = get_object_or_404(User, username=user)
    this_landlord = get_object_or_404(Landlord, user=this_user)
    rooms = Room.objects.order_by(
        '-list_date').filter(landlord=this_landlord)
    context = {
        'rooms': rooms
    }
    return render(request, 'landlord/dashboard.html', context)


def get_inquiry(request, room_id):
    inquiries = Inquiry.objects.filter(room_id=room_id)
    context = {
        'inquiries': inquiries
    }
    return render(request, 'landlord/inquiries.html', context)


def moderator_dashboard(request):
    user = request.user
    users = User.objects.all()
    active_users = User.objects.filter(is_active=True)
    unapproved_rooms = Room.objects.filter(
        is_approved=False)
    advertisements = Room.objects.filter(is_approved=True, is_available=True)
    context = {
        'user': user,
        'users': users,
        'active_users': active_users,
        'unapproved_rooms': unapproved_rooms,
        'advertisements': advertisements
    }
    return render(request, 'moderator/dashboard.html', context)


def view_rooms(request):
    rooms = Room.objects.filter(is_approved=False)
    context = {
        'rooms': rooms
    }
    return render(request, 'moderator/rooms.html', context)


def approve_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    room.is_approved = True
    room.status = 'approved'
    room.save()
    rooms = Room.objects.filter(is_approved=False, status='under review')
    context = {
        'rooms': rooms
    }
    return render(request, 'moderator/rooms.html', context)


def dissaprove_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    room.is_approved = False
    room.status = 'rejected'
    room.save()
    rooms = Room.objects.filter(is_approved=False, status='under review')
    context = {
        'rooms': rooms
    }
    return render(request, 'moderator/rooms.html', context)
