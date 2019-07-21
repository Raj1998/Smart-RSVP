from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils.safestring import mark_safe
from .models import Booking, Event
from django.db.models import Sum
import hashlib
import qrcode
import os
# from io import StringIO
# from django.core.files.uploadedfile import InMemoryUploadedFile


def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('register_login')


def home(request):
    if request.user.is_authenticated:
        max_rsvp = Booking.objects.all().filter(user=request.user).aggregate(Sum('max_rsvp'))['max_rsvp__sum']
        done_rsvp = Booking.objects.all().filter(user=request.user).aggregate(Sum('done_rsvp'))['done_rsvp__sum']
        params = {'max': max_rsvp, 'done': done_rsvp}
        return render(request, 'home.html', params)
    else:
        return redirect('register_login')


def book(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            current_user = request.user
            events = Event.objects.all().filter(user=current_user)
            if len(events) == 0:
                messages.info(request, "Please add at least one event then proceed further.")
                return redirect('event')
            else:
                params = {'events': events}
                return render(request, 'addRecord.html', params)
        else:
            name = request.POST.get('name')
            e_id = request.POST.get('event_id')
            maxRsvp = int(request.POST.get('maxRSVP'))
            user = request.user
            event = Event.objects.get(event_id=e_id)

            # print(name)
            # print(func)
            # print(maxRsvp)

            message = name + event.event_name
            digest = hashlib.md5(message.encode()).hexdigest()

            # change localhost to your static IP or website base url
            # for example
            # url = "http://192.168.43.90:8000/rsvp?bid="+digest

            if "ON_HEROKU" in os.environ:
                url = "https://django-app-241.herokuapp.com/rsvp?bid=" + digest
            else:
                url = "http://localhost:8000/rsvp?bid="+digest

            if not Booking.objects.filter(digest=digest):
                qr = qrcode.make(url)
                base_path = os.getcwd() + "/media/rsvp/"
                entry = Booking(guest_name=name,
                                user= user,
                                event= event,
                                max_rsvp=maxRsvp,
                                done_rsvp=maxRsvp,
                                digest=digest,
                                url=url
                                )
                entry.save()
                i = entry.booking_id
                file_name = str(i) + ".jpg"
                qr.save(base_path + file_name)

                Booking.objects.filter(booking_id=entry.booking_id).update(qrcode="rsvp/" + file_name)
                return HttpResponse("data inserted...<a href='/'>back</a>")
            else:
                ss = "oops! duplicate data found (Guest name already in this event).... try again... <a href='/book'>back</a>"
                return HttpResponse(ss)
    else:
        return redirect('register_login')


def viewAll(request):
    if request.user.is_authenticated:
        user = request.user
        id = request.GET.get('eid')
        if id:
            event = Event.objects.get(event_id=id)
            events = Event.objects.all().filter(user=user)
            all_bookings = Booking.objects.all().filter(event=event, user=user)
            params = {'all': all_bookings, 'events': events, 'eid': int(id)}
            return render(request, 'viewAll.html', params)

        all_bookings = Booking.objects.all().filter(user=user)
        events = Event.objects.all().filter(user=user)
        params = { 'all': all_bookings, 'events': events }
        return render(request, 'viewAll.html', params)
    else:
        return redirect('register_login')


def event(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, 'newEvent.html')
        else:
            current_user = request.user
            # print(current_user)
            event_name = request.POST['name']
            event_desc = request.POST['desc']
            new_event = Event(
                            event_name=event_name,
                            event_desc=event_desc,
                            user=current_user
                        )
            new_event.save()
            msg = "New event is added, now you can add invites in it. <a href='/book'>here</a>"
            messages.info(request, mark_safe(msg))
            return redirect('event')
    else:
        return redirect('register_login')


def rsvp(request):
    id = request.GET.get('bid')
    if id is None or len(id) != 32:
        res = "<h1>Invalid url ...</h1>"
        return HttpResponse(res)
    else:
        try:
            guest = Booking.objects.get(digest=id)
            params = {'name':guest.guest_name,
                      'host_name': guest.user.username,
                      'function':guest.event.event_name,
                      'desc': guest.event.event_desc,
                      'max': guest.max_rsvp,
                      'digest':guest.digest,
                      'range':range(0, guest.max_rsvp+1)}
            return render(request, 'welcome.html', params)
        except:
            res = "<h1>record not found</h1>"
            return HttpResponse(res)


def done(request):
    number = int(request.POST.get('number'))
    digest = request.POST.get('digest')
    try:
        Booking.objects.filter(digest=digest).update(done_rsvp = number)
        res = "<h1>Updation Done. Thank you</h1>"
    except:
        res = "<h1>Something went wrong...!</h1>"
    return HttpResponse(res)


def register_login(request):
    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'register_login.html', context)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("try again with different username and/or password... <a href='/'>here</a>")
    else:
        return HttpResponse("method not allowed")


def login_method(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("try again... <a href='/'>here</a>")
    else:
        return HttpResponse("Method not allowed")


def logout_method(request):
    logout(request)
    messages.info(request, "Logged out")
    return redirect('index')