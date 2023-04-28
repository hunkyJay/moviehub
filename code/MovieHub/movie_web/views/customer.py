from django.shortcuts import redirect, render
from django.http import HttpResponse
from my_admin.models import Customer
from django.core.paginator import Paginator
from datetime import date, datetime
import hashlib
import random

# Create your views here.


# Load user information edit form
def edit(request):
    try:
        current_username = request.session['logineduser'].get('username')
        ob = Customer.objects.get(username=current_username)
        context = {'customer': ob}
        return render(request, 'movie_web/customer/edit.html', context)
    except Exception as err:
        print(err)
        context = {'info': 'Cannot find the information of current user'}
    return render(request, 'movie_web/info.html', context)


# Update user information
def update(request):
    try:
        current_username = request.POST["username"]
        ob = Customer.objects.get(username=current_username)
        ob.name = request.POST['name']
        password = request.POST['password']

        # If typing to change password
        if password != '':
            password_salt = ob.password_salt
            password_seed = password + password_salt
            md5 = hashlib.md5()
            md5.update(password_seed.encode('utf-8'))
            ob.password_hash = md5.hexdigest()

        phone = request.POST['phone']
        ob.phone = int(phone)
        ob.email = request.POST['email']
        ob.bank_card = request.POST['bank_card']
        ob.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "Update Successfully"}
        ob = Customer.objects.get(username=current_username)
        request.session['logineduser'] = ob.toDict()
    except Exception as err:
        print(err)
        context = {'info': 'Update Failed'}
    return render(request, 'movie_web/info.html', context)