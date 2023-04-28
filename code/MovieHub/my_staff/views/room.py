import random

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from my_admin.models import Room
from django.core.paginator import Paginator
from datetime import datetime
import hashlib
import string


# browse room information
def index(request, pIndex=1):
    model = Room.objects
    roomList = model.all()
    keyWord = request.GET.get("keyword", None)
    condition = []

    # keyword research
    if keyWord:
        if is_number(keyWord):
            id = int(keyWord)
            roomList = roomList.filter(room_id=id)
        condition.append('keyword=' + keyWord)

    # In page by 10 record
    pIndex = int(pIndex)
    page = Paginator(roomList, 10)
    maxPages = page.num_pages
    if pIndex > maxPages:
        pIndex = maxPages
    if pIndex < 1:
        pIndex = 1
    roomList2 = page.page(pIndex)  # acquire current page info
    pageNum = page.page_range  # acquire num of page
    context = {"roomList": roomList2, 'pageNum': pageNum, 'pIndex': pIndex, 'maxPages': maxPages,
               'condition': condition}
    for room in roomList:
        print(room.toDict())
    return render(request, 'my_staff/room/index.html', context)


# load room addition form
def add(request):
    return render(request, 'my_staff/room/add.html')


# insert new room action
def insert(request):
    try:
        ob = Room()
        ob.room_id = request.POST['roomId']
        ob.row_size = request.POST['rowSize']
        ob.column_size = request.POST['columnSize']
        ob.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        context = {'info': "Add new room successfully"}
        ob.save()
    except Exception as err:
        print(err)
        context = {'info': "Add new room fails, the room id has been used,please use another roomId"}
    return render(request, 'my_staff/info.html', context)


# load room edit form
def edit(request, roomId=0):
    try:
        ob = Room.objects.get(room_id=roomId)
        context = {'room': ob}
        return render(request, 'my_staff/room/edit.html', context)
    except Exception as err:
        print(err)
        context = {'info': 'Cannot find the information of room'}
    return render(request, 'my_staff/info.html', context)


# update room information action
def update(request):
    try:
        roomId = request.POST["roomId"]
        ob = Room.objects.get(room_id=roomId)
        ob.row_size = request.POST['rowSize']
        ob.column_size = request.POST['columnSize']
        ob.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "Update Room Successfully"}
        return render(request, 'my_staff/info.html', context)
    except Exception as err:
        print(err)
        context = {'info': 'Update Room Failed'}
    return render(request, 'my_staff/info.html', context)


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
