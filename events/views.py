from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, UserUpdate, EventForm, BookingForm, ProfileForm
from django.contrib import messages
from .models import Event, Booking, Profile, Following
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home.html')

class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("public-events")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('my-events', user_id= request.user.id)
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")

def no_access(request):
    return render(request, 'no_access.html')


def my_events(request, user_id):
    if request.user.is_anonymous:
        return redirect('login')
    now = datetime.now()
    user = User.objects.get(id=user_id)
    events = Event.objects.filter(owner=user, date__gte=now)
    profile = Profile.objects.get(user=user)
    query = request.GET.get('q')
    if query:
        events = events.filter(
            Q(name__icontains=query)|
            Q(description__icontains=query)|
            Q(owner__username__icontains=query)
        ).distinct()
    following = False
    if Following.objects.filter(profile__user=user, follower=request.user).exists():
        following = True
    followers = Following.objects.filter(profile__user=user)
    followers_number = 0
    for follower in followers:
        followers_number += 1
    context = {
       "events": events,
       "user": user,
       "profile": profile,
       "followers_number": followers_number,
       "following": following,
    }
    return render(request, 'myevents.html', context)

def booked_events(request):
    if request.user.is_anonymous:
        return redirect('login')
    now = datetime.now()
    bookings = Booking.objects.filter(user=request.user, event__date__gte=now)
    context = {
       "bookings": bookings,
    }
    return render(request, 'bookedevents.html', context)

def history_events(request, user_id):
    if request.user.is_anonymous:
        return redirect('login')
    user = User.objects.get(id=user_id)
    now = datetime.now()
    bookings = Booking.objects.filter(user=user, event__date__lte=now)
    events = Event.objects.filter(owner=user,date__lte=now)
    context = {
       "bookings": bookings,
       "user":user,
       "events": events,
    }
    return render(request, 'history.html', context)

def profile_page(request, user_id):
    if request.user.is_anonymous:
        return redirect('login')
    now = datetime.now()
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)
    bookings = Booking.objects.filter(user=user, event__date__gte=now)
    history = Booking.objects.filter(user=user, event__date__lte=now)
    events = Event.objects.filter(owner=user,date__gte=now)
    followers = Following.objects.filter(profile__user=user)
    context = {
       "bookings": bookings,
       "history": history,
       "events": events,
       "followers": followers,
       "user":user,
       "profile":profile,

    }
    return render(request, 'userprofile.html', context)

def public_events(request):
    if request.user.is_anonymous:
        return redirect('home')
    now = datetime.now()
    events = Event.objects.filter(date__gte=now)
    query = request.GET.get('q')
    if query:
        events = events.filter(
            Q(name__icontains=query)|
            Q(description__icontains=query)|
            Q(owner__username__icontains=query)
        ).distinct()

    context = {
       "events": events,
    }
    return render(request, 'publicevents.html', context)


def create_event(request):
    if request.user.is_anonymous:
        return redirect('signin')
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event.save()
            return redirect('my-events', user_id= request.user.id)
    context = {
        "form":form,
    }
    return render(request, 'createevent.html', context)


def update_event(request, event_id):
    event_obj = Event.objects.get(id=event_id)
    if not (request.user.is_staff or request.user == event_obj.owner):
        return redirect('no-access')
    form = EventForm(instance=event_obj)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event_obj)
        if form.is_valid():
            form.save()
            return redirect('public-events')
    context = {
        "event_obj": event_obj,
        "form":form,
    }
    return render(request, 'eventupdate.html', context)


def update_profile(request, user_id):
    if not (request.user.is_authenticated):
        return redirect('login')
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)
    form_a = ProfileForm(instance=profile)
    form_b = UserUpdate(instance=profile)
    if request.method == "POST":
        form_a = ProfileForm(request.POST, request.FILES, instance=profile)
        form_b = UserUpdate(request.POST, instance=user)
        if (form_a.is_valid() and form_b.is_valid()):
            form_a.save()
            form_b.save()
            messages.success(request, "Profile successfully update!")
            return redirect('my-events', user_id= user.id)
    context = {
        "form_a": form_a,
        "form_b":form_b,
        "user":user,
        "profile":profile,
    }
    return render(request, 'userprofile.html', context)

def delete_event(request, event_id):
    event_obj = Event.objects.get(id=event_id)
    if not (request.user == event_obj.owner):
        return redirect('no-access')
    event_obj.delete()
    return redirect('my-events', user_id= user.id)



def detail_event(request, event_id):
    if request.user.is_anonymous:
        return redirect('home')
    event = Event.objects.get(id=event_id)
    bookings = Booking.objects.filter(event=event)
    context = {
        "event": event,
        "bookings": bookings
    }
    return render(request, 'eventdetail.html', context)

def book_event(request, event_id):
    event_obj = Event.objects.get(id=event_id)

    if request.user.is_anonymous:
        return redirect('home')
    if request.user == event_obj.owner:
        messages.warning(request, "You can't book your own event!")
        return redirect('public-events')
    else:
        seats = int(request.POST.get("seats"))
        if seats == 0:
            messages.warning(request, "You must choose a valid seat number!")
            return redirect('public-events') 
        if event_obj.available_tickets - seats < 0:
            messages.warning(request, "There are not enough seats for your booking!")
            return redirect('public-events')
        event_obj.available_tickets -= seats
        event_obj.save()
        booking = Booking.objects.create(event=event_obj,user=request.user, seats=seats)
        messages.success(request, "Event successfully booked!")
    return redirect('public-events')




def user_follow(request, user_id):
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)
    if request.user.is_anonymous:
        return redirect('signin')
    
    follow, created = Following.objects.get_or_create(profile=profile, follower=request.user)
    if created:
        action="follow"
    else:
        follow.delete()
        action="unfollow"

    followers = Following.objects.filter(profile__user=user)
    followers_number = 0
    for follower in followers:
        followers_number += 1
    response = {
        "action": action,
        "followers_number": followers_number,
    }
    return JsonResponse(response, safe=False)



