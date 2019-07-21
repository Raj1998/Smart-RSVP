from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Booking
from django.db.models import Sum
import hashlib
import qrcode
import os
# from io import StringIO
# from django.core.files.uploadedfile import InMemoryUploadedFile


def index(request):
    max_rsvp = Booking.objects.aggregate(Sum('max_rsvp'))['max_rsvp__sum']
    done_rsvp = Booking.objects.aggregate(Sum('done_rsvp'))['done_rsvp__sum']
    params = {'max': max_rsvp, 'done': done_rsvp}
    return render(request, 'home.html', params)


def book(request):
    return render(request, 'addRecord.html')


def viewAll(request):
    all_bookings = Booking.objects.all()
    params = { 'all': all_bookings }
    return render(request, 'viewAll.html', params)


def insert(request):
    name = request.POST.get('name')
    func = request.POST.get('function_name')
    maxRsvp = int(request.POST.get('maxRSVP'))
    # print(name)
    # print(func)
    # print(maxRsvp)

    message = name+func
    digest = hashlib.md5(message.encode()).hexdigest()

    # change localhost to your static IP or website base url
    # for example
    # url = "http://192.168.43.90:8000/rsvp?bid="+digest

    # url = "http://localhost:8000/rsvp?bid="+digest
    url = "https://django-app-241.herokuapp.com/rsvp?bid="+digest
    if not Booking.objects.filter(digest=digest):
        qr = qrcode.make(url)
        base_path = os.getcwd()+"/media/rsvp/"
        entry = Booking(guest_name=name,
                        function_name=func,
                        max_rsvp=maxRsvp,
                        done_rsvp=maxRsvp,
                        digest=digest,
                        url=url
                        )
        entry.save()
        i = entry.booking_id
        file_name = str(i)+".jpg"
        qr.save(base_path + file_name)

        Booking.objects.filter(booking_id=entry.booking_id).update(qrcode="rsvp/"+file_name)
        return HttpResponse("data inserted...<a href='/'>back</a>")
    else:
        return HttpResponse("oops duplicate data.... try again... <a href='/book'>back</a>")


def rsvp(request):
    id = request.GET.get('bid')
    if id == None or len(id)!=32:
        res = "<h1>Invalid url ...</h1>"
        return HttpResponse(res)
    else:
        try:
            guest = Booking.objects.get(digest=id)
            params = {'name':guest.guest_name,
                      'function':guest.function_name,
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
            return HttpResponse("try again")

    else:
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'register.html', context)


def login_method(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
           return redirect('login')
    else:
        return render(request, 'login.html')


def logout_method(request):
    logout(request)
    messages.info(request, "Logged out")
    return redirect('index')