from django.shortcuts import render, redirect
from django.urls import reverse
import random
from PIL import Image, ImageDraw, ImageFont
import hashlib

from my_admin.models import Staff
from my_admin.models import Announcement
from my_admin.models import Customer
from my_admin.models import Order
from datetime import datetime, timedelta
# Create your views here.
from django.http import HttpResponse


# Create your views here.
def index(request):
    now = datetime.now()
    zeroToday = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                microseconds=now.microsecond)
    beforeWeek = now - timedelta(days=7)
    staffs = Staff.objects
    numOfStaff = staffs.all().__len__()
    customers = Customer.objects
    numOfCustomers = customers.all().filter(create_time__gte=beforeWeek).__len__()
    announcements = Announcement.objects
    todayAnnouncement = announcements.all().filter(create_time__gte=zeroToday).__len__()
    orders = Order.objects.all().filter(create_time__gte=beforeWeek)
    numOfOrder = orders.__len__()
    revenue = 0
    for order in orders:
        revenue = revenue + order.price

    context = {'numOfStaff': numOfStaff, 'numOfTodayAnnouncement': todayAnnouncement, 'numOfCustomer': numOfCustomers,
               'numOfOrder': numOfOrder, 'revenue': revenue}

    return render(request, 'my_admin/index/homepage.html', context)


def loadLogin(request):
    return render(request, 'my_admin/index/loadLogin.html')


def login(request):
    try:
        staffId = request.POST["staffId"]
        password = request.POST["password"]
        ob = Staff.objects.get(staff_id=staffId)
        md5 = hashlib.md5()
        password_seed = request.POST["password"] + ob.password_salt
        md5.update(password_seed.encode('utf-8'))
        if request.POST["verifyCode"] != request.session["verifyCode"]:
            context = {'info': 'verify code is wrong'}
            return render(request, "my_admin/index/loadLogin.html", context)
        if md5.hexdigest() == ob.password_hash and ob.level == 2:
            request.session['adminuser'] = ob.toDict()
            return redirect(reverse('admin_homepage'))
        elif md5.hexdigest() == ob.password_hash and ob.level != 2:
            context = {'info': 'no permission'}
        else:
            context = {'info': 'password is incorrect'}
    except Exception as err:
        print(err)
        context = {'info': 'StaffId is invalid '}

    return render(request, "my_admin/index/loadLogin.html", context)


def logout(request):
    del request.session['adminuser']
    return redirect(reverse('admin_load_login'))


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
