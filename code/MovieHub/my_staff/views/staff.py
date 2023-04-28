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
    page = Paginator(staffList, 5)
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
    return render(request, 'my_staff/staff/index.html', context)







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
