from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
    path("book/", views.book, name="booking"),
    path("event", views.event, name="event"),
    path("insertData/", views.insert, name="insertion"),
    path("rsvp/", views.rsvp, name="rsvp"),
    path("done/", views.done, name="done"),
    path("viewAll/", views.viewAll, name="viewAll"),
    path("register_login/", views.register_login, name="register_login"),
    path("register", views.register, name="register"),
    path("login", views.login_method, name="login"),
    path("logout", views.logout_method, name="logout"),

]
