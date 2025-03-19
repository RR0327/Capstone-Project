from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .models import (
    User,
    CafeteriaMenu, 
    BusRoute, 
    bus_schedule,
    Faculty, 
    Course, 
    ClassSchedule, 
    Club, 
    Event,
    CampusBuilding
)

def index(request):
    return render(request, 'index.html')

# ---------------------
# Authentication Views
# ---------------------
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def register_view(request):
    """
    Handles user registration and automatically generates a Card with a QR code.
    """
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        email = request.POST.get('email').strip()
        role = request.POST.get('role')
        password = request.POST.get('password')
        id_number = request.POST.get('id_number').strip()
        level = request.POST.get('level') if role == 'student' else None
        term = request.POST.get('term') if role == 'student' else None
        contact_information = request.POST.get('contact_information').strip()
        
        if not all([name, email, role, password, id_number, contact_information]):
            messages.error(request, "All fields are required.")
            return redirect('register')
        
        if role == 'student' and not all([level, term]):
            messages.error(request, "Level and Term are required for students.")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect('register')

        if User.objects.filter(id_number=id_number).exists():
            messages.error(request, "This ID number is already registered.")
            return redirect('register')
        
        try:
            user = User.objects.create_user(
                email=email, name=name, role=role,
                id_number=id_number, level=level, term=term,
                contact_information=contact_information, password=password
            )
            # Card.objects.create(user=user)
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error during registration: {str(e)}")
            return redirect('register')
    
    return render(request, 'register.html')




def user_logout(request):
    logout(request)
    return redirect('login')

# ---------------------
# 1) Cafeteria Menus
# ---------------------
def cafeteria_view(request):
    today = date.today()
    menus = CafeteriaMenu.objects.filter(day=today)
    context = {
        'menus': menus,
        'today': today
    }
    return render(request, 'cafeteria.html', context)

# ---------------------
# 2) Bus Routes & Schedules
# ---------------------
def bus_schedules_view(request):
    routes = BusRoute.objects.all()
    schedules = bus_schedule.objects.all()
    context = {
        'routes': routes,
        'schedules': schedules
    }
    return render(request, 'bus_schedules.html', context)

# ---------------------
# 3) Class Schedules & Faculty Contacts
# ---------------------
@login_required
def class_schedules_view(request):
    # If you want to fetch class schedules for the currently logged in user, 
    # you'd create a relationship with User. For simplicity, show all:
    schedules = ClassSchedule.objects.all()
    faculty = Faculty.objects.all()
    courses = Course.objects.all()
    context = {
        'schedules': schedules,
        'faculty': faculty,
        'courses': courses
    }
    return render(request, 'class_schedules.html', context)

# ---------------------
# 4) Events & Clubs
# ---------------------
def events_view(request):
    clubs = Club.objects.all()
    events = Event.objects.all().order_by('event_date')
    context = {
        'clubs': clubs,
        'events': events
    }
    return render(request, 'events.html', context)

# ---------------------
# 5) (Optional) Campus Navigation 
# ---------------------
def campus_map_view(request):
    buildings = CampusBuilding.objects.all()
    context = {
        'buildings': buildings
    }
    return render(request, 'campus_map.html', context)

# Example JSON endpoint if you need data for an AR or interactive map
def buildings_json(request):
    buildings_data = list(CampusBuilding.objects.all().values())
    return JsonResponse(buildings_data, safe=False)
