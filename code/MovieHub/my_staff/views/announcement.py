import random

from django.shortcuts import render

# Create your views here.
from my_admin.models import Announcement
from django.core.paginator import Paginator
from datetime import datetime


# browse announcement information
def index(request, pIndex=1):
    model = Announcement.objects
    announcementList = model.all().order_by('-create_time')
    keyWord = request.GET.get("keyword", None)
    condition = []

    # keyword research
    if keyWord:
        announcementList = announcementList.filter(content__contains=keyWord)
        condition.append('keyword=' + keyWord)

    # In page by 10 record
    pIndex = int(pIndex)
    page = Paginator(announcementList, 10)
    maxPages = page.num_pages
    if pIndex > maxPages:
        pIndex = maxPages
    if pIndex < 1:
        pIndex = 1
    announcementList2 = page.page(pIndex)  # acquire current page info
    pageNum = page.page_range  # acquire num of page
    context = {"announcementList": announcementList2, 'pageNum': pageNum, 'pIndex': pIndex, 'maxPages': maxPages,
               'condition': condition}
    for announcement in announcementList:
        print(announcement.toDict())
    return render(request, 'my_staff/announcement/index.html', context)


# load announcement information addition form
def add(request):
    return render(request, 'my_staff/announcement/add.html')


# insert new announcement action
def insert(request):
    try:
        ob = Announcement()
        while True:
            announcement_id = random.randint(10000000, 99999999)
            try:
                announcement = Announcement.objects.get(announcement_id=announcement_id)
            except Exception as err:
                ob.announcement_id = announcement_id
                break
            else:
                continue

        ob.content = request.POST['content']
        ob.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        context = {'info': "Post announcement successfully"}
        ob.save()
    except Exception as err:
        print(err)
        context = {'info': "Post announcement fails"}
    return render(request, 'my_staff/info.html', context)


# delete announcement action
def delete(request, announcementId=0):
    try:
        ob = Announcement.objects.get(announcement_id=announcementId)
        ob.delete()
        context = {'info': 'Successfully deleted'}
    except Exception as err:
        context = {'info': 'Delete fails'}
    return render(request, 'my_staff/info.html', context)

