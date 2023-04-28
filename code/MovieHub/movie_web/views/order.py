from platform import release
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from my_admin.models import Order
from my_admin.models import Release
from django.db.models import Q
from django.core import serializers
from my_staff.models import Seat
from django.utils import timezone
import json

def index(request, pIndex=1):
    username = request.session['logineduser']['username']
    model = Order.objects
    orderList = model.all()
    orderList = orderList.filter(customer_username=username)
    condition = []
    # In page by 10 record 
    pIndex = int(pIndex)
    page = Paginator(orderList, 10)
    maxPages = page.num_pages
    if pIndex > maxPages:
        pIndex = maxPages
    if pIndex < 1:
        pIndex = 1
    orderList2 = page.page(pIndex)  # acquire current page info
    for obj in orderList2:
        if(obj.is_cancel==1):
            continue
        limitTime = obj.release_time - timedelta(minutes=15)
        print(limitTime.tzinfo)
        print(datetime.now().tzinfo)
        print(timezone.now().tzinfo)
        limitTime=limitTime.replace(tzinfo=None)
        print(limitTime)
        print(datetime.now())
        print(timezone.now())
        print(limitTime < datetime.now())
        if(limitTime < datetime.now()):
            obj.is_cancel = 2
    pageNum = page.page_range  # acquire num of page
    context = {"orderList": orderList2, 'pageNum': pageNum, 'pIndex': pIndex, 'maxPages': maxPages,
               'condition': condition}
    return render(request, 'movie_web/order/index.html', context)

def cancel(request):
    model = Order.objects
    orderList = model.all()
    id = request.POST.get("order_id", None)
    print(id)
    orderList = orderList.filter(order_id=id)
    if(len(orderList)!=1):
        return JsonResponse({'info':'cancel failed!'})
    order = orderList[0]
    order.is_cancel = 1
    order.save()
    seat_content = order.seat_content
    release_id = order.release_id
    seats = seat_content.split(" ")
    for seat in seats:  
        print(seat)
        row = seat[4]
        column = seat[6]
        seatList = Seat.objects.all().filter(Q(row_id=row) & Q(column_id=column)& Q(release_id=release_id))
        if(len(seatList)!=1):
            return JsonResponse({'info':'cancel failed!'})
        seatList[0].is_available = 0
        seatList[0].save()
    return JsonResponse({'info':'Successfully Canceled!'})