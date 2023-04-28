from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import random
from PIL import Image, ImageDraw, ImageFont
import hashlib
import re
from my_admin.models import Customer, Movie, Order

from datetime import datetime, timedelta
from my_admin.models import Announcement

# Create your views here.

# The initial welcome page
def index(request):
    return render(request, "movie_web/welcomePage.html")

# Load user register form
def register(request):
    return render(request, "movie_web/index/register.html")

# Do register
def doRegister(request):
    try:
        ob = Customer()
        username = request.POST["username"]
        password = request.POST["password"]
        name = request.POST['name']
        email = request.POST['email']

        # Existing username
        try:
            customer = Customer.objects.get(username = username)
        except Exception as err:
            ob.username = username
        else:
            context = {'info': 'username already exists'}
            return render(request, "movie_web/index/register.html", context)
        
        # Invalid input
        if not re.search(u'^[_a-zA-Z0-9\u4e00-\u9fa5]+$', username) or len(username)==0 or len(username)>20:
            context = {'info': 'Username must be within 20 characters'}
            return render(request, "movie_web/index/register.html", context)
        if not re.search(u'^[A-Za-z]+$', name) or len(name)==0 or len(name)>20:
            context = {'info': 'Name must be within 20 characters'}
            return render(request, "movie_web/index/register.html", context)
        if not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) or len(email)==0 :
            context = {'info': 'Email is invalid'}
            return render(request, "movie_web/index/register.html", context)
        if request.POST["verifyCode"] != request.session["verifyCode"]:
            context = {'info': 'verify code is wrong'}
            return render(request, "movie_web/index/register.html", context)
        
        n = random.randint(100000, 999999)
        ob.password_salt = n
        md5 = hashlib.md5()
        password_seed = password + str(n)
        md5.update(password_seed.encode('utf-8'))
        ob.password_hash = md5.hexdigest()
        ob.name = name
        ob.email = email
        ob.save()
        return redirect(reverse('customer_load_login'))
    except Exception as err:
        print(err)
        context = {'info': "Register fails"}
    return render(request, 'movie_web/index/register.html', context)

# Load user login form
def loadLogin(request):
    return render(request, 'movie_web/index/loadLogin.html')

# Receive login request
def login(request):
    try:
        username = request.POST["username"]
        password = request.POST["password"]
        ob = Customer.objects.get(username=username)
        md5 = hashlib.md5()
        password_seed = password + ob.password_salt
        md5.update(password_seed.encode('utf-8'))
        if request.POST["verifyCode"] != request.session["verifyCode"]:
            context = {'info': 'verify code is wrong'}
            return render(request, "movie_web/index/loadLogin.html", context)
        if md5.hexdigest() == ob.password_hash:
            request.session['logineduser'] = ob.toDict()
            return redirect(reverse('customer_home'))
        else:
            context = {'info': 'password is incorrect'}
    except Exception as err:
        print(err)
        context = {'info': 'username is invalid '}

    return render(request, "movie_web/index/loadLogin.html", context)

# Receive logout request
def logout(request):
    del request.session['logineduser']
    return redirect(reverse('customer_load_login'))

# Get the verify code
def verify(request):
    bgcolor = (242, 164, 247)
    width = 100
    height = 25
    im = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(im)
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    str1 = '0123456789'
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    font = ImageFont.truetype('static/Arial.ttf', 21)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -3), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -3), rand_str[3], font=font, fill=fontcolor)
    del draw
    request.session['verifyCode'] = rand_str
    import io
    buf = io.BytesIO()
    im.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')


def home(request):
    movie_obs = Movie.objects
    order_obs = Order.objects
    num_of_movies = movie_obs.all().__len__()
    num_of_orders = order_obs.all().__len__()
    now = datetime.now()
    zero_today = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                microseconds=now.microsecond)
    announcements = Announcement.objects
    today_announcement = announcements.all().filter(create_time__gte=zero_today).__len__()
    context = {'numOfMovies': num_of_movies, 'numOfOrders':num_of_orders, 'numOfTodayAnnouncement': today_announcement}

    return render(request, 'movie_web/index/homepage.html', context)
