from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Event, club_panel, Communication, Room, RoomBooking, BudgetRequest
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User




def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to dashboard after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
    

#Jilan code
def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            clubs = club_panel.objects.all()
            
            events = Event.objects.all()

            return render(request, 'oca_dashboard.html', {'clubs': clubs, 'events': events})
        else:
            return render(request, 'ClubPanel/dashboard.html')
    return render(request, 'home.html')

def club_detail(request, club_id):
    club = club_panel.objects.get(id=club_id)
    pending_events = Event.objects.filter(club=club, status='PENDING')
    budgets = BudgetRequest.objects.filter(status = 'PENDING')

    return render(request, 'club detail.html', {'club': club, 'events': pending_events, 'budgets':budgets })

def approve_event(request, event_id):
    if request.method == "POST":
        event = get_object_or_404(Event, id=event_id)
        print(event)
        if event.status == "PENDING":
            event.status = "APPROVED"
            event.save()
            messages.success(request, f"The event '{event.title}' has been approved.")
        else:
            messages.warning(request, "This event is already approved.")
    return redirect('home')

def approve_budget(request, budget_id):

    if request.method == "POST":
        budget = get_object_or_404(BudgetRequest, id=budget_id)
        
        if BudgetRequest.status == "PENDING":
            BudgetRequest.status = "APPROVED"
            BudgetRequest.save()
            messages.success(request, f"The event '{BudgetRequest.event.title}' has been approved.")
        else:
            messages.warning(request, "This event is already approved.")
            
    return redirect('home')

@login_required
def messaging(request, club_id=None):
    # If the user is OCA (staff), they can view messages with a specific club
    if request.user.is_staff and club_id:
        club = get_object_or_404(User, id=club_id)
        messages = Communication.objects.filter(
            (Q(from_user=request.user) & Q(to_user=club)) |
            (Q(from_user=club) & Q(to_user=request.user))
        ).order_by('timestamp')
    else:
        # For clubs, only allow messaging between the club and OCA
        oca_user = User.objects.filter(is_superuser=True).first()
        club = request.user
        messages = Communication.objects.filter(
            (Q(from_user=club) & Q(to_user=oca_user)) |
            (Q(from_user=oca_user) & Q(to_user=club))
        ).order_by('timestamp')

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')
        if request.user.is_superuser:
            to_user = club
        else:
            to_user = User.objects.filter(is_superuser=True).first()

        Communication.objects.create(
            from_user=request.user,
            to_user=to_user,
            subject=subject,
            message=message_text,
            timestamp=timezone.now()
        )
        if request.user.is_superuser:
            return redirect('messaging_club', club_id=club_id)
        else: 
            return redirect('messaging')
    

    return render(request, 'messaging.html', {
        'messages': messages,
        'club': club,
    })

#end of Jilan code

@login_required
def add_event(request):
    
    if request.method == 'POST':
        club_id = request.user.club_panel.id
        title = request.POST.get('title')
        description = request.POST.get('description')
        startdate = request.POST.get('end_date')
        enddate = request.POST.get('start_date')

        # Basic validation example (you can add more checks as needed)
        if club_id and title:
            event = Event(
                club=club_panel.objects.get(id=club_id),
                title=title,
                description=description,
                start_time=startdate,
                end_time=enddate,
                status='PENDING',
            )
            event.save()
        return redirect('event_management')
    
    return render(request, 'ClubPanel/add_event.html')


@login_required
def event_management(request):
    events = Event.objects.filter(club=request.user.club_panel)
    return render(request, 'ClubPanel/event_management.html', {'events': events})

@login_required
def room_booking(request):
    return render(request, 'ClubPanel/room_booking.html')


@login_required
def room_booking_form(request):
    # Fetch available rooms
    rooms = Room.objects.all()

    if request.method == 'POST':
        room_id = request.POST.get('room')
        event_id = request.POST.get('event')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        purpose = request.POST.get('purpose')

        # Ensure required fields are provided
        if room_id and event_id and start_time and end_time:
            # Create a new RoomBooking object and save it
            room_booking = RoomBooking(
                room=Room.objects.get(id=room_id),
                event=Event.objects.get(id=event_id),
                start_time=start_time,
                end_time=end_time
            )
            room_booking.save()
            messages.success(request, "Room booking request submitted.")
        return redirect('room_booking')

    events = Event.objects.filter(club=request.user.club_panel)
    return render(request, 'ClubPanel/room_booking_form.html', {'rooms': rooms, 'events': events})


@login_required
def budget_form(request):
    # Fetch events specific to the current user's club
    events = Event.objects.filter(club=request.user.club_panel)

    if request.method == 'POST':
        event_id = request.POST.get('event')
        amount_requested = request.POST.get('amount_requested')
        budget_description = request.POST.get('budget_description')

        # Save the form submission as a new budget request
        if event_id and amount_requested:
            budget_request = BudgetRequest(
                event=Event.objects.get(id=event_id),
                amount_requested=amount_requested,
                budget_description=budget_description,
                status='PENDING'
            )
            budget_request.save()
            messages.success(request, "Budget request submitted.")
        return redirect('budget_management')

    return render(request, 'ClubPanel/budget_form.html', {'events': events})


@login_required
def budget_management(request):
    # Display all budget requests associated with events created by the club panel
    budget_requests = BudgetRequest.objects.filter(event__club=request.user.club_panel)
    return render(request, 'ClubPanel/budget_management.html', {'budget_requests': budget_requests})



