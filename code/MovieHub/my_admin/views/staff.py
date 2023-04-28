import random

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from my_admin.models import Staff
from django.core.paginator import Paginator
from datetime import datetime
import hashlib
import string


# browse staff information
def index(request, pIndex=1):
    model = Staff.objects
    staffList = model.all()
    keyWord = request.GET.get("keyword", None)
    condition = []

    # keyword research
    if keyWord:
        if is_number(keyWord):
            id = int(keyWord)
            staffList = staffList.filter(staff_id=id)
        else:
            staffList = staffList.filter(name__contains=keyWord)
        condition.append('keyword=' + keyWord)

    # In page by 10 record
    pIndex = int(pIndex)
    page = Paginator(staffList, 10)
    maxPages = page.num_pages
    if pIndex > maxPages:
        pIndex = maxPages
    if pIndex < 1:
        pIndex = 1
    staffList2 = page.page(pIndex)  # acquire current page info
    pageNum = page.page_range  # acquire num of page
    context = {"staffList": staffList2, 'pageNum': pageNum, 'pIndex': pIndex, 'maxPages': maxPages,
               'condition': condition}
    for st in staffList:
        print(st.toDict())
    return render(request, 'my_admin/staff/index.html', context)


# load employee information addition form
def add(request):
    return render(request, 'my_admin/staff/add.html')


# insert new staff action
def insert(request):
    try:
        ob = Staff()
        while True:
            staff_id = random.randint(10000000, 99999999)
            try:
                staff = Staff.objects.get(staff_id=staff_id)
            except Exception as err:
                ob.staff_id = staff_id
                break
            else:
                continue

        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        password_seed = "12345678"+str(n)
        md5.update(password_seed.encode('utf-8'))
        ob.password_hash = md5.hexdigest()
        ob.password_salt = n
        ob.name = request.POST['name']
        level = request.POST['level']
        if level == "staff":
            ob.level = 0
        elif level == "manager":
            ob.level = 1
        elif level == "admin":
            ob.level = 2
        else:
            context = {'info': "Add new staff fails, invalid level"}
            return render(request, 'my_admin/info.html', context)
        phone = request.POST['phone']
        ob.phone = int(phone)
        ob.email = request.POST['email']
        ob.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        context = {'info': "Add new staff successfully, staff_id is %s, original password is 12345678" % ob.staff_id}
        ob.save()
    except Exception as err:
        print(err)
        context = {'info': "Add new staff fails"}
    return render(request, 'my_admin/info.html', context)


# delete staff action
def delete(request, staffId=0):
    try:
        ob = Staff.objects.get(staff_id=staffId)
        ob.delete()
        context = {'info': 'Successfully deleted'}
    except Exception as err:
        context = {'info': 'Delete fails'}
    return render(request, 'my_admin/info.html', context)


# load employee information edit form
def edit(request, staffId=0):
    try:
        ob = Staff.objects.get(staff_id=staffId)
        context = {'staff': ob}
        return render(request, 'my_admin/staff/edit.html', context)
    except Exception as err:
        print(err)
        context = {'info': 'Cannot find the information of edited staff'}
    return render(request, 'my_admin/info.html', context)

# update staff information action
def update(request):
    try:
        staffId = request.POST["staffId"]
        ob = Staff.objects.get(staff_id=staffId)
        ob.name = request.POST['name']
        password = request.POST['password']
        password_salt = ob.password_salt
        password_seed = password + password_salt
        md5 = hashlib.md5()
        md5.update(password_seed.encode('utf-8'))
        ob.password_hash = md5.hexdigest()
        level = request.POST['level']
        if level == "staff":
            ob.level = 0
        elif level == "manager":
            ob.level = 1
        elif level == "admin":
            ob.level = 2
        else:
            context = {'info': "update staff info fails, invalid level"}
            return render(request, 'my_admin/info.html', context)
        phone = request.POST['phone']
        ob.phone = int(phone)
        ob.email = request.POST['email']
        ob.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "Update Successfully"}
        return render(request, 'my_admin/info.html', context)
    except Exception as err:
        print(err)
        context = {'info': 'Update Failed'}
    return render(request, 'my_admin/info.html', context)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False
