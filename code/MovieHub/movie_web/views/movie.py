from platform import release
import random

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from datetime import datetime

from pymysql import NULL
from my_admin.models import Customer, Movie, Room, Release, Order
from my_staff.models import Seat
from django.db.models import Q
from django.core import serializers
import json


# Create your views here.

# browse movie information
def index(request, pIndex=1):
    model = Movie.objects
    movieList = model.all()
    keyWord = request.GET.get("keyword", None)
    condition = []

    # keyword research
    if keyWord:
        movieList = movieList.filter(
            Q(movie_name__icontains=keyWord) | Q(type__icontains=keyWord) | Q(cast__icontains=keyWord))
        condition.append('keyword=' + keyWord)

    # In page by 10 record
    pIndex = int(pIndex)
    page = Paginator(movieList, 5)
    maxPages = page.num_pages
    if pIndex > maxPages:
        pIndex = maxPages
    if pIndex < 1:
        pIndex = 1
    movieList2 = page.page(pIndex)  # acquire current page info
    pageNum = page.page_range  # acquire num of page
    context = {"movieList": movieList2, 'pageNum': pageNum, 'pIndex': pIndex, 'maxPages': maxPages,
               'condition': condition}
    for st in movieList:
        print(st)
    return render(request, 'movie_web/movie/index.html', context)


def releaseList(request, pIndex=1):
    model = Release.objects
    releaseList = model.all()
    id = request.POST.get("movie_id", None)
    print(id)
    condition = []
    now_time = datetime.now()
    # keyword research
    if id:
        releaseList = releaseList.filter(Q(movie_id=id)&Q(release_time__gte=now_time))
        condition.append('movie_id=' + id)

    # In page by 10 record
    pIndex = int(pIndex)
    page = Paginator(releaseList, 5)
    maxPages = page.num_pages
    if pIndex > maxPages:
        pIndex = maxPages
    if pIndex < 1:
        pIndex = 1
    releaseList2 = page.page(pIndex)  # acquire current page info
    pageNum = page.page_range  # acquire num of page
    print(pageNum)
    context = {"releaseList": [],
               'pageNum': list(pageNum),
               'pIndex': int(pIndex),
               'maxPages': int(maxPages),
               'condition': condition}
    for st in releaseList:
        print(st)
    json_data = serializers.serialize('json', releaseList2)  # json serialize
    context['releaseList'] = json_data
    return HttpResponse(json.dumps(context), content_type="application/json")


# load movie booking page
def loadBooking(request, release_id):
    release_id = int(release_id)
    print("release_id=")
    print(release_id)
    try:
        username = request.session['logineduser']['username']
        customer_ob = Customer.objects.get(username = username)
        bank_account = customer_ob.bank_card

        # If do not bind a bank card to account
        if bank_account is None:
            context = {'customer': customer_ob}
            return render(request, 'movie_web/customer/edit.html', context)


        # Selected movie to book
        release_ob = Release.objects.get(release_id=release_id)
        movie_id = release_ob.movie_id
        movie_ob = Movie.objects.get(movie_id=movie_id)
        movie_name = movie_ob.movie_name
        room_id = release_ob.room_id
        room_ob = Room.objects.get(room_id=room_id)
        row_size = room_ob.row_size
        column_size = room_ob.column_size
        price = release_ob.price
        release_time = release_ob.release_time
        

        seat_obs = Seat.objects.filter(release_id=release_id)
        rows = range(1, row_size + 1)
        columns = range(1, column_size + 1)
        seat_list = []
        for row in rows:
            row_seat_obs = seat_obs.filter(row_id=row)
            row_seats = []
            for column in columns:
                seat_ob = row_seat_obs.get(column_id=column)
                seat = seat_ob.toDict()
                row_seats.append(seat)
            seat_list.append(row_seats)

        context = {'movie_name': movie_name, 'bank_account': bank_account, 'release_id': release_id,
                   'seat_list': seat_list, 'price': price, 'release_time': release_time}

        return render(request, 'movie_web/movie/ticketBooking.html', context)
    except Exception as err:
        print(err)
        context = {'info': 'Cannot book the movie'}
    return render(request, 'movie_web/movie/ticketBooking.html', context)


def bookMovie(request):
    releaseId = request.POST['release_id']
    seatContent = request.POST['seat_content']
    seatList = seatContent.split(' ')
    numOfSeat = seatList.__len__()
    username = request.session['logineduser']['username']
    releaseObject = Release.objects.get(release_id=releaseId)
    movieName = Movie.objects.get(movie_id=releaseObject.movie_id).movie_name
    price = releaseObject.price
    totalPrice = price * numOfSeat

    try:
        ob = Order()
        ob.order_id = random.randint(10000000, 99999999)
        ob.customer_username = username
        ob.room_id = releaseObject.room_id
        ob.seat_content = seatContent
        ob.seat_num = numOfSeat
        ob.release_id = releaseId
        ob.movie_name = movieName
        ob.price = totalPrice
        ob.is_cancel = 0
        # ob.is_pay = 0
        ob.release_time = releaseObject.release_time
        ob.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        
        for seat in seatList:
            row = seat[4]
            column = seat[6]
            seatObject = Seat.objects.get(release_id=releaseId, row_id=row, column_id=column)
            seatObject.is_available = 1
            seatObject.save()

    except Exception as err:
        print(err)
        return JsonResponse({'info': 'booking failed'})
        
    return JsonResponse({'info': 'successfully booked, view details in the order page '})
