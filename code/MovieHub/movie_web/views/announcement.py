import random

from django.shortcuts import render

from my_admin.models import Announcement
from django.core.paginator import Paginator
from datetime import datetime
# Create your views here.

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
    return render(request, 'movie_web/announcement/index.html', context)

def view(request, announcementId=0):
    try:
        ob = Announcement.objects.get(announcement_id=announcementId)
        content = ob.content
        context = {'info': content}
    except Exception as err:
        context = {'info': 'Invalid notice'}
    return render(request, 'movie_web/info.html', context)
